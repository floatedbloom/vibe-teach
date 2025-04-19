import streamlit as st
import plotly.express as px
import json

def view_student_page(student_name):
    st.title(f"Student Profile: {student_name}")

    st.subheader("Knowledge Overview")
    subjects = ["Math", "Science", "History", "English", "Art"]
    knowledge = [80, 70, 60, 90, 50]  # Placeholder values
    fig = px.line_polar(r=dict(zip(subjects, knowledge)), theta=subjects, line_close=True)
    st.plotly_chart(fig)

    # Scrollable list of completed assignments
    st.subheader("Completed Assignments")
    try:
        with open("assignments.json", "r") as file:
            assignments_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        assignments_data = []

    completed_assignments = [a for a in assignments_data if a.get("student_name") == student_name]
    completed_assignments.sort(key=lambda x: x.get("completion_date", ""))  # Sort by date

    for assignment in completed_assignments:
        st.write(f"- {assignment.get('name', 'Unnamed Assignment')} (Completed on: {assignment.get('completion_date', 'Unknown Date')})")

    # AI-generated summary of performance
    st.subheader("Performance Summary")
    st.write("This is a placeholder for an AI-generated summary of the student's performance.")