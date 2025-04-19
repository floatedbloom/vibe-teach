import streamlit as st
from streamlit_slickgrid import st_slickgrid

st.title("Teacher Dashboard")
st.subheader("AP Computer Science A")

classes = [
    {
        "class_name": "AP Computer Science A",
        "students": [
            {"name": "Alice Johnson", "grade": "A", "status": "Present"},
            {"name": "Bob Smith", "grade": "B", "status": "Absent"},
            {"name": "Charlie Brown", "grade": "C", "status": "Present"},
            {"name": "Diana Prince", "grade": "A", "status": "Present"},
        ]
    }
]

columns = [
    {"id": "name", "name": "Name", "field": "name"},
    {"id": "grade", "name": "Grade", "field": "grade"},
    {"id": "status", "name": "Status", "field": "status"}
]

# Display class cards
for class_data in classes:
    if st.button(class_data['class_name']):
        st.subheader(f"Students in {class_data['class_name']}")
        # Render the student list in a SlickGrid table
        st_slickgrid(columns=columns, data=class_data['students'], key=class_data['class_name'])