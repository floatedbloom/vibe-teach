import uuid
import json
import tools
import data_types

class_name = "Algebra"


def get_uuid():
    return str(uuid.uuid4())


async def add_document(filename: str, page_images: list[str]):
    try:
        with open("documents.json", "r") as file:
            documents_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        documents_data = []

    new_document = await tools.read_document_from_images(page_images, filename=filename)
    documents_data.append(new_document)

    with open("documents.json", "w") as file:
        json.dump(documents_data, file, indent=4)


def add_assignment(
    name: str, assignment_type: str, additional_grading_instructions: str
):
    new_assignment = {
        "name": name,
        "rubrics": [],
        "assignment_type": assignment_type,
        "additional_grading_instructions": additional_grading_instructions,
        "submission_ids": [],
        "id": get_uuid(),
    }
    try:
        with open("assignments.json", "r") as f:
            assignments_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        assignments_data = []

    assignments_data.append(new_assignment)

    with open("assignments.json", "w") as f:
        json.dump(assignments_data, f, indent=4)


def add_student(name: str):
    new_student = {
        "name": name,
        "analysis_summary": "",
        "recent_submissions": "",
        "class": class_name,
        "completed_assignments": [],
        "id": get_uuid(),
    }
    try:
        with open("students.json", "r") as file:
            students_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        students_data = []
    students_data.append(new_student)

    # Save the updated list back to the JSON file
    with open("students.json", "w") as file:
        json.dump(students_data, file, indent=4)


def generate_submission():
    new_submission = {
        "submission_documents": [],
        "text": "",
        "grading_analysis": "",
        "analysis_summary": "",
        "grade": None,
        "student_id": "",
        "id": get_uuid(),
    }


def get_students():
    try:
        with open("students.json", "r") as file:
            students_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        students_data = []

    return students_data


def get_assignments():
    try:
        with open("assignments.json", "r") as file:
            assignments_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        assignments_data = []

    return assignments_data


"""
class_json = {
    {
        "name" : "AP Placeholder",
        "assignments_ids" : [],
        "student_ids" : [],
        "class_info" : [],
        "custom_instructions" : "",
        "analysis_chat_history" : [],
    }
}

assignments_json = {
    {
        "name" : "",
        "rubrics" : [],
        "assignment_type" : "",
        "additional_grading_instructions" : "",
        "submissions_ids" : [],
        "id" : ""
    }
}

submissions_json = {
    {
        "submission_documents" : [],
        "text" : "",
        "grading_analysis" : "",
        "analysis_summary" : "",
        "grade" : ,
        "student_id" : "",
        "id" : "",
    }
}

students_json = {
    {
        "name" : "",
        "analysis_summary" : "",
        "recent_submissions" : "",
        "class" : "",
        "completed_assignments" : [],
        "id" : ""
    }
}

documents_json = {
    {
        "filename" : "",
        "page_images" : [],
        "text" : "",
        "id" : "",
    }
}
"""

