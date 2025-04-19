import fitz  # pip install pymupdf
import base64
import uuid
from openai import AsyncOpenAI
from copy import deepcopy
import json
import tempfile,os,base64
import docx2pdf  # pip install docx2pdf

from data_types import *

from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI()

async def read_document_from_images(page_images: list[DataURL], *, filename: str) -> Document:
    """
    Reads a document from a list of images in Data URL format.
    """
    prompt_text = (
        "Extract *ALL TEXT AND INFORMATION* from the images IN MARKDOWN FORMAT. If there are multiple pages, always extract the text from each page."
        "Not using any python or anything but using your own vision capabilities."
        "If the images are pages of a PDF, they will be in order."
        "No newlines within tables, use <br> instead."
        "No surrounding ``` for markdown, just the markdown."
        "Ensure the markdown is formatted correctly, especially tables."
        "Read math notation using latex format."
        "ALWAYS INDICATE IN THE MARKDOWN WHICH MCQ OPTIONS ARE BOXED OR SELECTED."
    )
    content = [{"type": "input_text", "text": prompt_text}]
    for image_data_url in page_images:
        content.append({"type": "input_image", "image_url": image_data_url, 'detail': 'high'})

    response = await client.responses.create(
        model='o4-mini',
        input=[{'role': 'user', 'content': content}],
    )

    return {
        'id': str(uuid.uuid4()),
        'page_images': page_images,
        'filename': filename,
        'text': response.output_text,
    }
    

async def read_document_from_pdf(pdf_bytes: bytes, *, filename: str) -> Document:
    """
    Reads a document from a PDF file by converting PDF pages to images and then using the read_document_from_images function.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap()
        images.append('data:image/png;base64,' + base64.b64encode(pix.tobytes("png")).decode("utf-8"))
    return await read_document_from_images(images, filename=filename)

def docx_to_png_dataurls(docx_bytes):
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
        tmp.write(docx_bytes);docx_path=tmp.name
    pdf_path=docx_path.removesuffix('.docx')+'.pdf'; docx2pdf.convert(docx_path,pdf_path)
    urls=[]
    with fitz.open(pdf_path) as doc:
        for page in doc:
            png_bytes=page.get_pixmap().tobytes('png')
            urls.append('data:image/png;base64,'+base64.b64encode(png_bytes).decode())
            with open(str(uuid.uuid4())+'.png', 'wb') as f:
                f.write(png_bytes)
    os.remove(docx_path);os.remove(pdf_path)
    return urls

async def read_document_from_docx(docx_bytes: bytes, *, filename: str) -> Document:
    """
    Reads a document from a DOCX file by converting DOCX pages to images and then using the read_document_from_images function.
    """
    return await read_document_from_images(docx_to_png_dataurls(docx_bytes), filename=filename)

async def read_document(file_bytes: bytes, *, filename: str) -> Document:
    '''
    Reads a file of either PDF, DOCX, PNG, JPG, or JPEG format into a Document.
    '''

    if filename.lower().endswith('.docx'):
        return await read_document_from_docx(file_bytes, filename=filename)
    if filename.lower().endswith('.pdf'):
        return await read_document_from_pdf(file_bytes, filename=filename)
    if filename.lower().endswith('.png'):
        return await read_document_from_images(['data:image/png;base64,'+base64.b64encode(file_bytes).decode()], filename=filename)
    if filename.lower().endswith(('.jpg', '.jpeg')):
        return await read_document_from_images(['data:image/jpeg;base64,'+base64.b64encode(file_bytes).decode()], filename=filename)
    
    raise ValueError(f'Unsupported file type: {filename}')

async def generate_submission_from_documents(documents: list[Document], *, assignment: Assignment, class_: Class) -> Submission:
    """
    Generates a student submission object from a list of student submission documents.
    """
    submission_text = "\n\n\n\n".join(document['filename'] + '\n\n' + document['text'] for document in documents)
    prompt_text = (
        "Generate an analysis of a student submission based on class information and rubric information if provided.\n"
        "If there is no rubric, solve problems or use your own knowledge/judgement to grade the submission.\n"
        "class_name=" + class_['name'] + "\n"
        "class_information=" + json.dumps(class_['class_information']) + "\n"
        "custom_class_instructions=" + json.dumps(class_['custom_instructions']) + "\n"
        "class_students=" + json.dumps(class_['students']) + "\n"
        "assignment_name=" + assignment['name'] + "\n"
        "assignment_type=" + assignment['assignment_type'] + "\n"
        "rubrics=" + json.dumps(assignment['rubrics']) + "\n"
        "additional_grading_instructions=" + json.dumps(assignment['additional_grading_instructions']) + "\n"
        "submission_text=" + submission_text
    )
    content = [{"type": "input_text", "text": prompt_text}]
    response = await client.responses.create(
        model='o4-mini',
        input=[{'role': 'user', 'content': content}],
        text={
            "format": {
                "type": "json_schema",
                "name": "submission",
                "schema": {
                    "type": "object",
                    "properties": {
                        "student_id": {
                            "type": "string",
                            "description": "Find the student's name in their submission, and find the student ID corresponding to that name, or empty string if not found."
                        },
                        "grading_analysis": {
                            "type": "string",
                            "description": "An in-depth analysis of the submission exactly according to the rubric if provided. Include insight onto the student's reasoning process as well as strengths and gaps."
                        },
                        "analysis_summary": {
                            "type": "string",
                            "description": "Summarize the analysis into a single sentence. Focus on strengths, gaps, and feedback for improvement."
                        },
                        "grade": {
                            "type": "string",
                            "description": "If a rubric or maximum points is provided, give a score according to the rubric. Otherwise give a percentage score."
                        },
                    },
                    "required": ["student_id", "grading_analysis", "analysis_summary", "grade"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
    )

    submission_data = json.loads(response.output_text)

    return {
        'id': str(uuid.uuid4()),
        'text': submission_text,
        'student_id': submission_data['student_id'] or None,
        'submission_documents': deepcopy(documents),
        'grading_analysis': submission_data['grading_analysis'],
        'analysis_summary': submission_data['analysis_summary'],
        'grade': submission_data['grade'],
    }

# async def generate_chat

async def main():
    # Create document from math.pdf and grade the document based off of assignment and class placeholder values
    with open('math.docx', 'rb') as f:
        pdf_bytes = f.read()
    document = await read_document_from_docx(pdf_bytes, filename='math.docx')
    print(f'{document=}')
    class_: Class = {
        'id': str(uuid.uuid4()),
        'name': 'Math',
        'students': [
            {
                'id': str(uuid.uuid4()),
                'name': 'Bob Ross',
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'George Lapin',
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Steve Heimler',
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Jane Doe',
            },
        ],
        'assignments': [],
        'class_information': [],
        'custom_instructions': '',
        'analysis_chat_history': [],
    }
    assignment: Assignment = {
        'id': str(uuid.uuid4()),
        'name': 'Probability Wksht',
        'rubrics': [],
        'assignment_type': 'summative',
        'additional_grading_instructions': '',
        'submission_ids': [],
    }
    submission = await generate_submission_from_documents([document], assignment=assignment, class_=class_)
    print(f'{submission=}')

    with open('submission.json', 'w') as f:
        json.dump(submission, f, indent=4)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

