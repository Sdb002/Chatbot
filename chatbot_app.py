import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Chatbot",
    page_icon="💬",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* { box-sizing: border-box; }

html, body { margin: 0; padding: 0; }

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.main .block-container {
    background-color: #f0ede8 !important;
    font-family: 'Inter', sans-serif !important;
    color: #2c2825 !important;
}

.block-container {
    max-width: 720px !important;
    padding: 1.5rem 1.5rem 6rem !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* HEADER */
.app-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2c2825;
    letter-spacing: -0.02em;
    padding: 1rem 0 0.5rem;
    border-bottom: 1px solid #ddd9d2;
    margin-bottom: 1.5rem;
}

/* CHAT BUBBLES */
.msg-row {
    display: flex;
    gap: 0.6rem;
    margin-bottom: 0.9rem;
    align-items: flex-end;
}
.msg-row.user { flex-direction: row-reverse; }

.msg-bubble {
    max-width: 70%;
    padding: 0.7rem 0.95rem;
    border-radius: 18px;
    font-size: 0.9rem;
    line-height: 1.6;
    word-wrap: break-word;
    white-space: pre-wrap;
}
.msg-bubble.user {
    background: #4a7cf7;
    color: #fff;
    border-bottom-right-radius: 5px;
}
.msg-bubble.bot {
    background: #ffffff;
    color: #2c2825;
    border: 1px solid #e0dbd4;
    border-bottom-left-radius: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.msg-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-bottom: 2px;
}
.av-user { background: #4a7cf7; color: white; }
.av-bot  { background: #e8e4de; color: #6b6560; }

/* EMPTY STATE */
.empty-hint {
    text-align: center;
    color: #bbb5ae;
    font-size: 0.85rem;
    padding: 3rem 0;
}
.empty-hint span { font-size: 2rem; display: block; margin-bottom: 0.5rem; }

/* CHAT INPUT */
[data-testid="stBottom"] {
    background: #f0ede8 !important;
    border-top: 1px solid #ddd9d2 !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stBottom"] > div { background: #f0ede8 !important; }

.stChatInput > div {
    background: #ffffff !important;
    border: 1.5px solid #d8d3cc !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07) !important;
}
.stChatInput textarea {
    background: #ffffff !important;
    color: #2c2825 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
.stChatInput textarea::placeholder { color: #b0aaa3 !important; }
.stChatInput button {
    background: #4a7cf7 !important;
    border-radius: 10px !important;
    color: white !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] > div {
    background: #e8e4de !important;
    border-right: 1px solid #d5d0c8 !important;
}
section[data-testid="stSidebar"] * { color: #2c2825 !important; }
section[data-testid="stSidebar"] label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #6b6560 !important;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background: #f5f2ee !important;
    border: 1px solid #cdc8c0 !important;
    color: #2c2825 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #f5f2ee !important;
    border: 1px solid #cdc8c0 !important;
    border-radius: 8px !important;
    color: #2c2825 !important;
}

/* BUTTON */
.stButton > button {
    background: #4a7cf7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

hr { border-color: #d5d0c8 !important; }
.stSpinner > div { border-top-color: #4a7cf7 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #cdc8c0; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="sk-or-..."
    )

    model_options = {
        "DeepSeek Chat v3":  "deepseek/deepseek-chat-v3-0324",
        "GPT-4o mini":       "openai/gpt-4o-mini",
        "Claude 3.5 Haiku":  "anthropic/claude-3-5-haiku",
        "Llama 3.3 70B":     "meta-llama/llama-3.3-70b-instruct",
        "Gemini Flash 2.0":  "google/gemini-flash-2.0",
    }
    selected_model = model_options[st.selectbox("Model", list(model_options.keys()))]

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, concise, and friendly AI assistant.",
        height=100
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ── SESSION STATE ─────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="app-title">💬 Chatbot</div>', unsafe_allow_html=True)

# ── MESSAGES ─────────────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown("""
    <div class="empty-hint">
        <span>💬</span>
        Start a conversation
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div class="msg-avatar av-user">you</div>
                <div class="msg-bubble user">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
                <div class="msg-avatar av-bot">ai</div>
                <div class="msg-bubble bot">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ── INPUT ─────────────────────────────────────────────────
user_input = st.chat_input("Message...")

if user_input and user_input.strip():
    if not api_key.strip():
        st.error("⚠️ Add your OpenRouter API key in the sidebar.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        messages_to_send = []
        if system_prompt.strip():
            messages_to_send.append({"role": "system", "content": system_prompt.strip()})
        messages_to_send.extend(st.session_state.chat_history)

        with st.spinner("Thinking..."):
            try:
                client = OpenAI(api_key=api_key.strip(), base_url="https://openrouter.ai/api/v1")
                response = client.chat.completions.create(model=selected_model, messages=messages_to_send)
                bot_reply = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.session_state.chat_history.pop()

        st.rerun()
