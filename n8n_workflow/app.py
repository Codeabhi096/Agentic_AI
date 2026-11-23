import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Determine default webhook URL (supports Streamlit secrets, env vars, or fallback)
DEFAULT_WEBHOOK_URL = "https://firstproject7208.app.n8n.cloud/webhook/783ce764-7ce6-4647-8de0-7c38ad0d4d21"

try:
    if "N8N_WEBHOOK_URL" in st.secrets:
        DEFAULT_WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]
except Exception:
    pass

DEFAULT_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", DEFAULT_WEBHOOK_URL)

# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("### n8n Connection")
    webhook_url = st.text_input(
        "Webhook URL:",
        value=DEFAULT_WEBHOOK_URL,
        help="Paste your test or production n8n webhook URL here."
    )
    
    st.divider()
    st.markdown("### 🛠️ Connected Tools")
    st.markdown("""
    - 🔍 **Google Search (SerpApi)**
    - 📅 **Google Calendar** (Events)
    - 📋 **Google Tasks** (To-do items)
    - ✉️ **Gmail** (Read & Send emails)
    - 📄 **Google Docs** (Notes & Docs)
    - 💰 **Expense Tracker** (Google Sheets & Calculator)
    """)
    
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Title
st.title("Personal AI Assistant")

# add subheader
st.subheader("What can your personal assistant do?")

# create a list of what your assistant can do
st.markdown("""
    1. Answer questions on various topics.
    2. Arrange Calendar events and meetings.
    3. Read your emails and send replies, can even summarize them for you.
    4. Manage your tasks and to-do lists.
    5. Take quick notes for you.
    6. Track your expenses and budgeting.
    """)

# add chats subheader
st.subheader("Chat with your assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask something from your assistant..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call n8n webhook and get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(webhook_url, json={"message": prompt}, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    # Handling various n8n response structures:
                    # e.g., [{"output": "..."}] or {"output": "..."}
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "output" in data[0]:
                        assistant_response = data[0]["output"]
                    elif isinstance(data, dict) and "output" in data:
                        assistant_response = data["output"]
                    elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
                        assistant_response = data[0]
                    elif isinstance(data, dict) and "text" in data:
                        assistant_response = data["text"]
                    else:
                        assistant_response = str(data)
                        
                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    error_msg = f"⚠️ Error {response.status_code}: Unable to reach n8n assistant. Make sure your workflow is active or the test webhook is listening."
                    st.error(error_msg)
            except requests.exceptions.Timeout:
                st.error("⏳ Request timed out. The agent is taking longer to process the request.")
            except Exception as e:
                st.error(f"❌ Failed to connect to webhook: {e}")
