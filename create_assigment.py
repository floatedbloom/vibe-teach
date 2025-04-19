import streamlit as st

def create_assignment_page():
    st.title("Create Assignment")

    # Assignment Name
    assignment_name = st.text_input("Assignment Name")

    # Buttons to add rubrics
    st.subheader("Add Rubrics")
    if st.button("Add PDF Rubric"):
        st.write("PDF Rubric added.")
    if st.button("Add Image Rubric"):
        st.write("Image Rubric added.")

    # Formative vs Summative Toggle
    st.subheader("Assignment Type")
    assignment_type = st.radio("Select Assignment Type", ["Formative", "Summative"])

    # Additional Instructions
    st.subheader("Additional Instructions")
    additional_instructions = st.text_area("Enter any additional instructions for the assignment")

    # Buttons to add student submissions
    st.subheader("Add Student Submissions")
    if st.button("Add PDF Submission"):
        st.write("PDF Submission added.")
    if st.button("Add Image Submission"):
        st.write("Image Submission added.")

# Call the function to render the page
create_assignment_page()