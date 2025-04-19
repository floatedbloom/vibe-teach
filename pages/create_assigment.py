import streamlit as st
from funcs import add_assignment
import os
import json

def create_assignment_page():
    st.title("Create Assignment")

    # Assignment Name
    assignment_name = st.text_input("Assignment Name")

    # Formative vs Summative Toggle
    st.subheader("Assignment Type")
    assignment_type = st.radio("Select Assignment Type", ["Formative", "Summative"])

    # Additional Instructions
    st.subheader("Additional Instructions")
    additional_instructions = st.text_area("Enter any additional instructions for the assignment")

    # Category Dropdown Menu
    st.subheader("Select Group")
    try:
        # Load class data from JSON
        with open("classes.json", "r") as file:
            class_data = json.load(file)
            groups = [cls.get("group", "all") for cls in class_data]
    except (FileNotFoundError, json.JSONDecodeError):
        groups = ["all"]  # Default group if no data is available

    selected_group = st.selectbox("Choose a group for this assignment", groups)

    # File Uploads Section
    st.subheader("Upload Files")

    # Buttons to add rubrics
    st.subheader("Add Rubrics")
    uploaded_file = st.file_uploader("Upload Rubric File", type=["pdf", "png", "jpg", "docx"])
    if uploaded_file is not None:
        # Create a directory if it doesn't exist
        save_dir = "rubrics"
        os.makedirs(save_dir, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(save_dir, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
        
        st.success(f"File saved as {uploaded_file.name} in {save_dir}")

    # PDF Submission
    pdf_file = st.file_uploader("Upload PDF Submission", type=["pdf"])
    if pdf_file is not None:
        save_dir = "submissions/pdf"
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, pdf_file.name)
        with open(file_path, 'wb') as f:
            f.write(pdf_file.getvalue())
        st.success(f"PDF Submission saved as {pdf_file.name} in {save_dir}")

    # Image Submission
    image_file = st.file_uploader("Upload Image Submission", type=["png", "jpg", "jpeg"])
    if image_file is not None:
        save_dir = "submissions/images"
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, image_file.name)
        with open(file_path, 'wb') as f:
            f.write(image_file.getvalue())
        st.success(f"Image Submission saved as {image_file.name} in {save_dir}")

    # Create Assignment Button
    if st.button("Create Assignment"):
        st.write("Assignment created successfully!")
        add_assignment(assignment_name, assignment_type, additional_instructions, group=selected_group)

# Call the function to render the page
create_assignment_page()