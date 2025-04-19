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
    

    st.title("Chat Analysis")
    st.write("This is a synced chat analysis page. Refresh to see new messages from other users.")

    # Display chat messages from history on app rerun
    for message in (firebase_ref.child("chat_analysis_history").get() or {}).values():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        firebase_ref.child("chat_analysis_history").push({"role": "user", "content": prompt})

        response = asyncio.run(generate_chat_analysis(firebase_ref.child("chat_analysis_history").get()))
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        firebase_ref.child("chat_analysis_history").push({"role": "assistant", "content": response})



# Call the function to render the page
create_chat_analysis_page()
