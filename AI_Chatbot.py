import os
import streamlit as st
import google.genai as genai

# Initialize Gemini client
client = genai.Client()

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Chatbot Web App")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Display chat messages with bubbles
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0; width:fit-content;'>"
            f"<b>You:</b> {msg['content']}</div>", unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='background-color:#EAEAEA; padding:10px; border-radius:10px; margin:5px 0; width:fit-content;'>"
            f"<b>Gemini:</b> {msg['content']}</div>", unsafe_allow_html=True
        )
