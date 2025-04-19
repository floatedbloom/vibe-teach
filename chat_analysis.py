import streamlit as st
import numpy as np
import asyncio

from tools import generate_chat_analysis
from firebase_rtdb import firebase_ref

def create_chat_analysis_page():
    # ...
    
    
    # with st.chat_message("user"):
    #     st.write("Hello 👋")

    # with st.chat_message("assistant"):
    #     st.write("Hello human")
    #     st.bar_chart(np.random.randn(30, 3))

    st.write("This is a synced chat analysis page. Refresh to see new messages from other users.")

    chatbox = st.container(height=600)
    # Display chat messages from history on app rerun
    for message in (firebase_ref.child("chat_analysis_history").get() or {}).values():
        with chatbox.chat_message(message["role"]):
            chatbox.markdown(message["content"])
        
    # React to user input
    if prompt := st.chat_input("Enter query here"):
        # Display user message in chat message container
        with chatbox.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        firebase_ref.child("chat_analysis_history").push({"role": "user", "content": prompt})

        response = asyncio.run(generate_chat_analysis(firebase_ref.child("chat_analysis_history").get()))
        # Display assistant response in chat message container
        with chatbox.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        firebase_ref.child("chat_analysis_history").push({"role": "assistant", "content": response})



# Call the function to render the page
create_chat_analysis_page()
