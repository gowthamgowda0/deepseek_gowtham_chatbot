import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Function to call DeepSeek API
def get_deepseek_response(messages):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages
    }

    response = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="DeepSeek AI Chatbot", page_icon="🤖", layout="wide")

# Sidebar for chat history
st.sidebar.title("📜 Chat History")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today? 😊"}]
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []  # Store multiple chat sessions
if "current_chat_index" not in st.session_state:
    st.session_state.current_chat_index = None  # Track which chat is open

# Display new chat button at the top
if st.sidebar.button("➕ New Chat", use_container_width=True):
    if st.session_state.messages:  # Save current session
        st.session_state.chat_sessions.insert(0, st.session_state.messages.copy())  # Add to history (newest first)
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today? 😊"}]
    st.session_state.current_chat_index = None  # Reset current chat view

# Show chat history list (most recent first)
for i, session in enumerate(st.session_state.chat_sessions):
    chat_title = f"💬 Chat {len(st.session_state.chat_sessions) - i}"

    # Create a larger button using Markdown & CSS
    if st.sidebar.markdown(f"""
        <button style="
            width: 100%;
            height: 60px;
            font-size: 18px;
            text-align: center;
            border-radius: 8px;
            border: none;
            background-color: #4CAF50;
            color: white;
            margin-bottom: 10px;
            cursor: pointer;">
            {chat_title}
        </button>
    """, unsafe_allow_html=True):
        st.session_state.messages = session  # Load the selected chat
        st.session_state.current_chat_index = i  # Track which chat is open

# Main chat UI
st.title("🤖 Gowtham AI Chatbot")

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    with st.spinner("Thinking..."):
        start_time = time.time()
        response = get_deepseek_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        response_time = time.time() - start_time

# Display full chat history in the main area
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show response time for the last message
if user_input:
    st.caption(f"Response time: {response_time:.2f}s")
