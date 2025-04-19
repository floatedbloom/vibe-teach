import uuid
import json
import tools
from firebase_admin import db
from firebase_rtdb import firebase_ref
import os

class_name = "Algebra"


def get_uuid():
    return str(uuid.uuid4())


async def add_document(filename: str, page_images: list[str]):
    # Replace JSON loading with Firebase RTDB
    documents_ref = db.reference("documents")
    documents_data = documents_ref.get() or []

    new_document = await tools.read_document_from_images(page_images, filename=filename)
    documents_data.append(new_document)

    # Replace JSON saving with Firebase RTDB
    documents_ref.set(documents_data)


def add_assignment(
    name: str, assignment_type: str, additional_grading_instructions: str, group: str = "all"
):
    new_assignment = {
        "name": name,
        "rubrics": [],
        "assignment_type": assignment_type,
        "additional_grading_instructions": additional_grading_instructions,
        "submission_ids": [],
        "group": group,
        "id": get_uuid(),
    }
    # Replace JSON loading with Firebase RTDB
    assignments_ref = db.reference("assignments")
    assignments_data = assignments_ref.get() or []

    assignments_data.append(new_assignment)

    # Replace JSON saving with Firebase RTDB
    assignments_ref.set(assignments_data)


def add_student(name: str):
    new_student = {
        "name": name,
        "analysis_summary": "",
        "recent_submissions": "",
        "class": class_name,
        "completed_assignments": [],
        "id": get_uuid(),
    }
    # Replace JSON loading with Firebase RTDB
    students_ref = db.reference("students")
    students_data = students_ref.get() or []

    students_data.append(new_student)

    # Replace JSON saving with Firebase RTDB
    students_ref.set(students_data)


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
    # Replace JSON loading with Firebase RTDB
    students_ref = db.reference("students")
    students_data = students_ref.get() or []

    return students_data


def get_assignments():
    assignments_ref = db.reference("assignments")
    assignments_data = assignments_ref.get() or []

    return assignments_data

def create_groups():
    summaries = ""
    students = firebase_ref.get("students")
    for student in students:
        summaries += f"Student: {student['name']}\n"
        summaries += f"Completed Assignments: {', '.join(student['completed_assignments'])}\n\n"


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
        "group" : "",
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

