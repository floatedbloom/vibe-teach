import streamlit as st
from funcs import add_student, add_assignment, get_students, get_assignments

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

# Add a new assignment
with st.form("add_assignment_form"):
    assignment_title = st.text_input("Assignment Title")
    assignment_type = st.text_input("Assignment Type")
    additional_instructions = st.text_area("Additional Grading Instructions")
    submitted = st.form_submit_button("Add Assignment")
    if submitted and assignment_title and assignment_type:
        add_assignment(assignment_title, assignment_type, additional_instructions)
        st.success(f"Added assignment: {assignment_title}")

# Display list of assignments
assignments = get_assignments()
if assignments:
    st.subheader("Assignment List")
    for assignment in assignments:
        st.write(f"- {assignment['name']} (Type: {assignment['assignment_type']})")
else:
    st.info("No assignments added yet.")