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
    submitted = st.form_submit_button("Add Student")
    if submitted and student_name:
        add_student(student_name)
        st.success(f"Added student: {student_name}")

# Display list of students
students = get_students()
if students:
    st.subheader("Student List")
    with st.container(height = 300):
        for student in students:        
            st.write(f"**Name:** {student['name']}")
            st.divider()  # Add a horizontal line between items
else:
    st.info("No students added yet.")

# Assignments Section
st.subheader("Manage Assignments")

# Display list of assignments
assignments = get_assignments()
if assignments:
    st.subheader("Assignment List")
    with st.container():
        for assignment in assignments:
            st.write(f"**Name:** {assignment['name']}")
            st.write(f"**Type:** {assignment['assignment_type']}")
            st.divider()  # Add a horizontal line between items
else:
    st.info("No assignments added yet.")

page = st.Page("pages/create_assigment.py")
st.page_link(page, label="Add Assignments", icon="📝")
