import fitz  # pip install pymupdf
import base64
import uuid

from openai import AsyncOpenAI

from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI()


async def read_document_from_images(page_images: list[str], *, filename: str):
    """
    Reads a document from a list of images in Data URL format.
    """
    prompt_text = (
        "can you extract *everything* from the pdf in markdown format. make sure you extract everything from the images"
        "not using any python or anything but using your own model capabilities. "
        "i will send the pdf as images in order. no newlines within tables, use <br> instead."
        "No surrounding ``` for markdown, just the markdown"
        "Ensure the markdown is formatted correctly, especially tables"
    )
    content = [{"type": "input_text", "text": prompt_text}]
    for image_data_url in page_images:
        content.append(
            {"type": "input_image", "image_url": image_data_url, "detail": "high"}
        )

    response = await client.responses.create(
        model="o4-mini",
        input=[{"role": "user", "content": content}],
    )

    return {
        "id": str(uuid.uuid4()),
        "page_images": page_images,
        "filename": filename,
        "text": response.output_text,
    }


async def read_document_from_pdf(pdf_bytes: bytes, *, filename: str):
    """
    Reads a document from a PDF file by converting PDF pages to images and then using the read_document_from_images function.
    """
    doc = fitz.open(stream=bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap()
        images.append(
            "data:image/png;base64,"
            + base64.b64encode(pix.tobytes("png")).decode("utf-8")
        )
    return await read_document_from_images(images, filename=filename)
