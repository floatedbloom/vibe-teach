import streamlit as st
import st_pages as pages
from funcs import get_students, get_assignments, add_student

# Title of the app
st.header("Manage Classroom")

# Students Section
st.subheader("Manage Students")

# Add a new student
with st.form("add_student_form"):
    student_name = st.text_input("Student Name")
    class_name = st.text_input("Class Name")
    submitted = st.form_submit_button("Add Student")
    if submitted and student_name and class_name:
        add_student(student_name, class_name)
        st.success(f"Added student: {student_name}")

# Display list of students
students = get_students()
if students:
    st.subheader("Student List")
    for student in students:
        st.write(f"- {student['name']} (Class: {student['class']})")
else:
    st.info("No students added yet.")

# Assignments Section
st.subheader("Manage Assignments")

# Display list of assignments
assignments = get_assignments()
if assignments:
    st.subheader("Assignment List")
    for assignment in assignments:
        st.write(
            f"- {assignment['name']} (Type: {assignment['assignment_type']}, Group: {assignment.get('group', 'all')})"
        )
else:
    st.info("No assignments added yet.")

page = st.Page("pages/create_assigment.py")
st.page_link(page, label="Add Assignments", icon="📝")
