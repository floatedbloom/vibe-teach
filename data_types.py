from typing import TypedDict

type UUID = str
type DataURL = str

class Document(TypedDict):
    id: UUID
    page_images: list[DataURL]
    filename: str
    text: str

class Submission(TypedDict):
    id: UUID
    text: str
    student_id: UUID
    submission_documents: list[Document.__annotations__['id']]
    grading_analysis: str
    analysis_summary: str
    grade: float | None

class Student(TypedDict):
    id: UUID
    name: str
    analysis_summary: str
    recent_submission_ids: list[Submission.__annotations__['id']]

class Assignment(TypedDict):
    id: UUID
    name: str
    rubrics: list[Document.__annotations__['id']]
    assignment_type: str # 'formative' | 'summative'
    additional_grading_instructions: str
    submission_ids: list[Submission.__annotations__['id']]

class Class(TypedDict):
    id: UUID
    name: str
    students: list[Student.__annotations__['id']]
    assignments: list[Assignment.__annotations__['id']]
    class_information: list[Document.__annotations__['id']]
    custom_instructions: str
    analysis_chat_history: list[dict]
