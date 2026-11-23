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
    page_title="Personal AI Assistant | n8n Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Responsive Animated CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Background & Container Tweaks */
    .main .block-container {
        max-width: 960px;
        padding-top: 1.8rem;
        padding-bottom: 5rem;
    }

    /* Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulseGlow {
        0%, 100% {
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.45);
        }
        50% {
            box-shadow: 0 0 28px rgba(168, 85, 247, 0.7);
        }
    }

    @keyframes floatAnimation {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-4px); }
    }

    /* Hero Header Styling */
    .hero-container {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
        animation: fadeInUp 0.8s ease-out;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #A5B4FC;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
        animation: pulseGlow 2s infinite ease-in-out;
    }

    /* Feature Cards Grid */
    .capabilities-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 12px;
        margin: 1.2rem 0 1.8rem 0;
        animation: fadeInUp 1s ease-out;
    }

    .cap-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(12px);
    }

    .cap-card:hover {
        transform: translateY(-3px) scale(1.02);
        border-color: rgba(168, 85, 247, 0.45);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
    }

    .cap-icon {
        font-size: 1.6rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 10px;
    }

    .cap-text h4 {
        margin: 0;
        font-size: 0.92rem;
        font-weight: 600;
        color: #F1F5F9;
    }

    .cap-text p {
        margin: 2px 0 0 0;
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.3;
    }

    /* Subheader styling */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.25rem;
        font-weight: 700;
        color: #E2E8F0;
        margin: 1.5rem 0 0.8rem 0;
    }

    /* Responsive Chat Messages */
    .stChatMessage {
        border-radius: 16px !important;
        margin-bottom: 12px !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease;
    }

    /* Quick suggestion buttons */
    .quick-title {
        font-size: 0.85rem;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Mobile Responsive Adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.9rem;
        }
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .capabilities-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    st.markdown("#### 🔗 n8n Webhook Configuration")
    webhook_url = st.text_input(
        "Live Webhook URL:",
        value=DEFAULT_WEBHOOK_URL,
        help="Paste your test or published n8n webhook URL here."
    )
    
    st.markdown("---")
    st.markdown("### 🛠️ Connected Tools & APIs")
    st.markdown("""
    - 🔍 **SerpApi** *(Live Google Search)*
    - 📅 **Google Calendar** *(Create & Manage Events)*
    - 📋 **Google Tasks** *(Smart To-Do Lists)*
    - ✉️ **Gmail** *(Inbox Reader & Email Sender)*
    - 📄 **Google Docs** *(Note-taking & Document Edits)*
    - 💰 **Expense Tracker** *(Google Sheets + Calculator)*
    - 🧠 **OpenAI LLM** + **Window Memory**
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    msg_count = len(st.session_state.get("messages", []))
    st.metric(label="Messages Exchanged", value=msg_count)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption("🚀 **Live App**: [Streamlit Cloud](https://agenticai-28f4o89zzdnxz2nwwqqtd2.streamlit.app/)")

# Hero Header with Live Pulse Badge
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span class="pulse-dot"></span>
        <span>n8n Multi-Agent Workflow Online</span>
    </div>
    <div class="hero-title">Personal AI Assistant</div>
    <p style="color: #94A3B8; font-size: 0.95rem; margin-top: 0;">
        Autonomous agent powered by OpenAI, n8n automations, and Google Workspace tools.
    </p>
</div>
""", unsafe_allow_html=True)

# Subheader: What can your personal assistant do?
st.markdown('<div class="section-title"><span>⚡</span> What can your personal assistant do?</div>', unsafe_allow_html=True)

# Dynamic Interactive Cards
st.markdown("""
<div class="capabilities-grid">
    <div class="cap-card">
        <div class="cap-icon">💡</div>
        <div class="cap-text">
            <h4>Answer Any Question</h4>
            <p>Researches deep queries with real-time web search via SerpApi.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">📅</div>
        <div class="cap-text">
            <h4>Calendar & Meetings</h4>
            <p>Schedules, checks, and manages Google Calendar events seamlessly.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">✉️</div>
        <div class="cap-text">
            <h4>Emails & Summaries</h4>
            <p>Reads Gmail inbox, summarizes threads, and drafts replies.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">📋</div>
        <div class="cap-text">
            <h4>Tasks & To-Do Lists</h4>
            <p>Organizes action items and checklists directly in Google Tasks.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">📝</div>
        <div class="cap-text">
            <h4>Quick Notes & Docs</h4>
            <p>Captures ideas and updates documents in Google Docs.</p>
        </div>
    </div>
    <div class="cap-card">
        <div class="cap-icon">💰</div>
        <div class="cap-text">
            <h4>Expense & Budgeting</h4>
            <p>Calculates and logs financial records directly into Google Sheets.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Section Header
st.markdown('<div class="section-title"><span>💬</span> Chat with your assistant</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Prompt Suggestions (Interactive buttons)
st.markdown('<div class="quick-title">✨ Try asking:</div>', unsafe_allow_html=True)
quick_cols = st.columns([1, 1, 1, 1])
clicked_prompt = None

with quick_cols[0]:
    if st.button("📅 My schedule today", use_container_width=True):
        clicked_prompt = "What events and meetings do I have on my calendar for today?"
with quick_cols[1]:
    if st.button("✉️ Check unread emails", use_container_width=True):
        clicked_prompt = "Can you check my latest unread emails in Gmail and summarize them?"
with quick_cols[2]:
    if st.button("💰 Log ₹350 coffee expense", use_container_width=True):
        clicked_prompt = "Log an expense of 350 INR for Coffee in my expense sheet."
with quick_cols[3]:
    if st.button("📋 Show my tasks", use_container_width=True):
        clicked_prompt = "Show my pending tasks in Google Tasks."

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Function to execute assistant response
def handle_assistant_interaction(user_input: str):
    # Display user message in chat message container
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call n8n webhook and get response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤖 Agent is thinking & executing tools..."):
            try:
                response = requests.post(webhook_url, json={"message": user_input}, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    # Handling various n8n response structures:
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
                    error_msg = f"⚠️ **Error {response.status_code}**: Unable to get response from n8n. Please ensure the workflow is published or active."
                    st.error(error_msg)
            except requests.exceptions.Timeout:
                st.error("⏳ **Request Timed Out**: The agent is taking longer to process the multi-step tools.")
            except Exception as e:
                st.error(f"❌ **Connection Error**: {e}")

# Trigger from quick button click or chat input
if clicked_prompt:
    handle_assistant_interaction(clicked_prompt)
    st.rerun()

if prompt := st.chat_input("Ask your assistant anything (e.g. 'Add a meeting tomorrow at 3 PM')..."):
    handle_assistant_interaction(prompt)
