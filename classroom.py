import streamlit as st
from funcs import get_students, get_assignments, add_student
from pages.view_student import view_student_page
import os  
import json

# Title of the app
st.header("Manage Classroom")

st.subheader("Add Class Documents")
uploaded_file = st.file_uploader("Upload File", type=["pdf", "png", "jpg", "docx"])
if uploaded_file is not None:
    # Create a directory if it doesn't exist
    save_dir = "class_docs"
    os.makedirs(save_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    st.success(f"File saved as {uploaded_file.name} in {save_dir}")

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
    with st.container(height=300):
        for student in students:
            # Create a button for each student
            if st.button(f"View {student['name']}", key=student['id']):
                # Update session state with the selected student's name
                st.session_state["selected_student"] = student["name"]
                # Debugging: Print the selected student
                print(f"Selected student: {st.session_state['selected_student']}")
                # Navigate to the view_student page
                st.switch_page("pages/view_student.py")
            st.divider()  # Add a horizontal line between items
else:
    st.info("No students added yet.")

# Assignments Section
st.subheader("Manage Assignments")

# Display list of assignments
assignments = get_assignments()
if assignments:
    st.subheader("Assignment List")
    with st.container(height=300):
        for assignment in assignments:
            st.write(f"**Name:** {assignment['name']}")
            st.write(f"**Type:** {assignment['assignment_type']}")
            st.divider()  # Add a horizontal line between items
else:
    st.info("No assignments added yet.")

# Button to navigate to the Create Assignment page
if st.button("Add Assignments"):
    st.switch_page("create_assignment")
