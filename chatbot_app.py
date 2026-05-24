import streamlit as st
from openai import OpenAI

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Chatbot",
    page_icon="💬",
    layout="centered"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #eae8e3 !important;
    color: #2c2825;
}
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.main .block-container {
    background-color: #eae8e3 !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* ---- App container ---- */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 6rem;
    max-width: 740px;
}

/* ---- Header ---- */
.chat-header {
    text-align: center;
    padding: 1.5rem 0 1.2rem;
    border-bottom: 1px solid #d5d1ca;
    margin-bottom: 1.5rem;
}
.chat-header h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1.6rem;
    letter-spacing: -0.03em;
    color: #2c2825;
    margin: 0;
}
.chat-header p {
    font-size: 0.72rem;
    color: #b0aaa0;
    margin-top: 0.35rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ---- Chat messages ---- */
.chat-bubble-wrapper {
    display: flex;
    margin-bottom: 1rem;
    gap: 0.65rem;
    align-items: flex-end;
}
.chat-bubble-wrapper.user { flex-direction: row-reverse; }

.avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.68rem;
    font-weight: 600;
    flex-shrink: 0;
}
.avatar.user-av { background: #4a7cf7; color: white; }
.avatar.bot-av  { background: #d5d1ca; color: #6b6560; }

.bubble {
    max-width: 72%;
    padding: 0.7rem 0.95rem;
    border-radius: 18px;
    font-size: 0.9rem;
    line-height: 1.65;
    word-wrap: break-word;
}
.bubble.user-bubble {
    background: #4a7cf7;
    color: #ffffff;
    border-bottom-right-radius: 4px;
}
.bubble.bot-bubble {
    background: #ffffff;
    border: 1px solid #dedad3;
    border-bottom-left-radius: 4px;
    color: #2a2a2a;
    white-space: pre-wrap;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* ---- Empty state ---- */
.empty-state {
    text-align: center;
    padding: 4rem 0;
    color: #c0bbb3;
}
.empty-state .icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    display: block;
}
.empty-state p {
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ---- Chat input ---- */
[data-testid="stBottom"] {
    background-color: #eae8e3 !important;
    border-top: 1px solid #d5d1ca !important;
    padding: 0.6rem 1rem !important;
}
[data-testid="stBottom"] > div {
    background-color: #eae8e3 !important;
}
.stChatInput > div {
    border: 1.5px solid #cdc9c2 !important;
    border-radius: 14px !important;
    background: #ffffff !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
.stChatInput textarea {
    background: #ffffff !important;
    color: #2c2825 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
.stChatInput textarea::placeholder { color: #aca8a0 !important; }
.stChatInput button {
    background: #4a7cf7 !important;
    border-radius: 10px !important;
    color: white !important;
}

/* ---- Buttons ---- */
.stButton > button {
    background: #4a7cf7 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.2rem !important;
    cursor: pointer !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] > div {
    background: #e0ddd7 !important;
    border-right: 1px solid #d0ccc5 !important;
}
section[data-testid="stSidebar"] label {
    color: #5a5550 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background: #f0ede8 !important;
    border: 1px solid #c8c4bc !important;
    color: #2c2825 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #f0ede8 !important;
    border: 1px solid #c8c4bc !important;
    border-radius: 8px !important;
    color: #2c2825 !important;
}

/* ---- Mobile expander ---- */
.streamlit-expanderHeader {
    background: #e0ddd7 !important;
    border-radius: 10px !important;
    border: 1px solid #d0ccc5 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #2c2825 !important;
}
.streamlit-expanderContent {
    background: #e8e5df !important;
    border: 1px solid #d0ccc5 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 0.8rem !important;
}
.streamlit-expanderContent input,
.streamlit-expanderContent textarea {
    background: #f0ede8 !important;
    border: 1px solid #c8c4bc !important;
    border-radius: 8px !important;
    color: #2c2825 !important;
}

hr { border-color: #d0ccc5 !important; margin: 1rem 0 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #4a7cf7 !important; }
.stSpinner p, div[data-testid="stSpinner"] * { color: #2c2825 !important; }

/* Expander text */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span { color: #2c2825 !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #c8c4bc; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# =========================================
# MODEL OPTIONS
# =========================================

model_options = {
    "DeepSeek Chat v3":  "deepseek/deepseek-chat-v3-0324",
    "GPT-4o mini":       "openai/gpt-4o-mini",
    "Claude 3.5 Haiku":  "anthropic/claude-3-5-haiku",
    "Llama 3.3 70B":     "meta-llama/llama-3.3-70b-instruct",
    "Gemini Flash 2.0":  "google/gemini-flash-2.0",
}


# =========================================
# SIDEBAR — desktop
# =========================================

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="sk-or-...",
        help="Get your key from openrouter.ai",
        key="sb_api_key"
    )

    selected_label = st.selectbox("Model", list(model_options.keys()), key="sb_model")
    selected_model = model_options[selected_label]

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, concise, and friendly AI assistant.",
        height=100,
        placeholder="Describe the AI's personality...",
        key="sb_system"
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True, key="sb_clear"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("""
    <div style="margin-top:1.5rem; text-align:center; font-size:0.7rem;
                color:#a0998f; letter-spacing:0.06em;">
        ⚡ POWERED BY OPENROUTER
    </div>
    """, unsafe_allow_html=True)


# =========================================
# SESSION STATE
# =========================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_ai" not in st.session_state:
    st.session_state.pending_ai = False


# =========================================
# HEADER
# =========================================

st.markdown("""
<div class="chat-header">
    <h1>💬 Chatbot</h1>
    <p>Powered by OpenRouter</p>
</div>
""", unsafe_allow_html=True)


# =========================================
# MOBILE SETTINGS — expander (visible on mobile, fine on desktop too)
# =========================================

with st.expander("⚙️ Settings", expanded=False):
    mb_api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="sk-or-...",
        key="mb_api_key"
    )
    mb_model_label = st.selectbox("Model", list(model_options.keys()), key="mb_model")
    mb_system = st.text_area(
        "System Prompt",
        value="You are a helpful, concise, and friendly AI assistant.",
        height=80,
        key="mb_system"
    )
    if st.button("🗑️ Clear Chat", use_container_width=True, key="mb_clear"):
        st.session_state.chat_history = []
        st.rerun()

# Sidebar takes priority over mobile expander
final_api_key      = api_key or mb_api_key
final_model        = model_options[selected_label]
final_system       = system_prompt or mb_system


# =========================================
# CHAT DISPLAY
# =========================================

if not st.session_state.chat_history:
    st.markdown("""
    <div class="empty-state">
        <span class="icon">💬</span>
        <p>Send a message to begin</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-bubble-wrapper user">
                <div class="avatar user-av">you</div>
                <div class="bubble user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bubble-wrapper">
                <div class="avatar bot-av">ai</div>
                <div class="bubble bot-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)


# =========================================
# INPUT AREA
# =========================================

user_input = st.chat_input("Type your message...")

# Step 1 — user sends message: save it, set pending flag, rerun to show bubble immediately
if user_input and user_input.strip():
    if not final_api_key.strip():
        st.error("⚠️ Please enter your OpenRouter API key in Settings.")
    else:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input.strip()
        })
        st.session_state.pending_ai = True
        st.rerun()  # <-- shows user bubble immediately


# =========================================
# STEP 2 — AI RESPONSE (runs after rerun shows user bubble)
# =========================================

if st.session_state.pending_ai:
    st.session_state.pending_ai = False

    messages_to_send = []
    if final_system.strip():
        messages_to_send.append({"role": "system", "content": final_system.strip()})
    messages_to_send.extend(st.session_state.chat_history)

    with st.spinner("Thinking..."):
        try:
            client = OpenAI(
                api_key=final_api_key.strip(),
                base_url="https://openrouter.ai/api/v1"
            )
            response = client.chat.completions.create(
                model=final_model,
                messages=messages_to_send
            )
            bot_reply = response.choices[0].message.content
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": bot_reply
            })
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")
            st.session_state.chat_history.pop()

    st.rerun()
