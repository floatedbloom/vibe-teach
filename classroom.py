import streamlit as st

# Title of the app

# Sidebar for navigation
st.header("Manage Classroom")
# Data storage (in-memory for simplicity)
if "students" not in st.session_state:
    st.session_state.students = []

if "assignments" not in st.session_state:
    st.session_state.assignments = []

# Students Section
if True:
    st.subheader("Manage Students")

    # Add a new student
    with st.form("add_student_form"):
        student_name = st.text_input("Student Name")
        submitted = st.form_submit_button("Add Student")
        if submitted and student_name:
            st.session_state.students.append(student_name)
            st.success(f"Added student: {student_name}")

    # Display list of students
    if st.session_state.students:
        st.subheader("Student List")
        for student in st.session_state.students:
            st.write(f"- {student}")
    else:
        st.info("No students added yet.")

    # Assignments Section
    st.subheader("Manage Assignments")

    # Add a new assignment
    with st.form("add_assignment_form"):
        assignment_title = st.text_input("Assignment Title")
        submitted = st.form_submit_button("Add Assignment")
        if submitted and assignment_title:
            st.session_state.assignments.append(assignment_title)
            st.success(f"Added assignment: {assignment_title}")

    # Display list of assignments
    if st.session_state.assignments:
        st.subheader("Assignment List")
        for assignment in st.session_state.assignments:
            st.write(f"- {assignment}")
    else:
        st.info("No assignments added yet.")
