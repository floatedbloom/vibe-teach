import streamlit as st
import plotly.express as px
import json

def view_student_page():
    # Get the student name from session state
    student_name = st.session_state.get("selected_student")

    if not student_name:
        st.error("No student selected. Please go back and select a student.")
        st.stop()  # Stop further execution

    st.title(f"Student Profile: {student_name}")

    # Load student data from JSON
    try:
        with open("students.json", "r") as file:
            students_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        students_data = []

    # Find the student by name
    student_data = next((s for s in students_data if s["name"] == student_name), None)

    if not student_data:
        st.error(f"Student '{student_name}' not found.")
        return

    # Knowledge Overview
    st.subheader("Knowledge Overview")
    topics = student_data.get("Topics", {})
    if topics:
        fig = px.line_polar(r=list(topics.values()), theta=list(topics.keys()), line_close=True)
        st.plotly_chart(fig)
    else:
        st.info("No knowledge data available for this student.")

    # Scrollable list of completed assignments
    st.subheader("Completed Assignments")
    completed_assignments = student_data.get("completed_assignments", [])
    if completed_assignments:
        for assignment in completed_assignments:
            st.write(f"- {assignment.get('name', 'Unnamed Assignment')} (Completed on: {assignment.get('completion_date', 'Unknown Date')})")
    else:
        st.info("No completed assignments available for this student.")

    # AI-generated summary of performance
    st.subheader("Performance Summary")
    performance_summary = student_data.get("analysis_summary", "No performance summary available.")
    st.write(performance_summary)


view_student_page()