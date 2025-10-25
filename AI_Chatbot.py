import streamlit as st
import google.genai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# ==========================
# === Load API Key ===
# ==========================
try:
    # Streamlit Cloud: use secrets
    api_key = st.secrets["GENAI_API_KEY"]
    st.write("✅ API key loaded from Streamlit secrets")
except Exception:
    # Local testing: load from key.env
    env_path = os.path.join(os.path.dirname(__file__), "key.env")
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("GENAI_API_KEY")
    if api_key:
        st.write("✅ API key loaded from key.env")
    else:
        st.error("❌ API key not found! Check key.env or Streamlit secrets.")
        st.stop()

# ==========================
# === Initialize Gemini client ===
# ==========================
client = genai.Client(api_key=api_key)

# ==========================
# === Streamlit UI Setup ===
# ==========================
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Chatbot Web App")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================
# === Chat input form ===
# ==========================
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    submit_button = st.form_submit_button("Send")

# Handle user input
if submit_button and user_input:
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": user_input, "time": timestamp})

    # Show typing indicator
    placeholder = st.empty()
    placeholder.markdown("<b>Gemini is typing...</b>", unsafe_allow_html=True)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({"role": "assistant", "content": response.text, "time": timestamp})
    except Exception as e:
        st.error(f"Error generating response: {e}")
    finally:
        placeholder.empty()

# ==========================
# === Display chat messages ===
# ==========================
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    timestamp = msg.get("time", "")

    if role == "user":
        st.markdown(
            f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0; width:fit-content; max-width:70%; box-shadow:2px 2px 5px #ccc;'>"
            f"<b>You ({timestamp}):</b> {content}</div>", unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='background-color:#EAEAEA; padding:10px; border-radius:10px; margin:5px 0; width:fit-content; max-width:70%; box-shadow:2px 2px 5px #ccc;'>"
            f"<b>Gemini ({timestamp}):</b> {content}</div>", unsafe_allow_html=True
        )

# ==========================
# === Save and Clear Buttons ===
# ==========================
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Save Chat"):
        if st.session_state.messages:
            df = pd.DataFrame(st.session_state.messages)
            df.to_csv("chat_history.csv", index=False)
            st.success("✅ Chat saved as chat_history.csv")
        else:
            st.warning("⚠️ No messages to save.")

with col2:
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
