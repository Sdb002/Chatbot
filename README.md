# 💬 Chatbot

A clean, multi-model AI chatbot built with Streamlit and powered by OpenRouter.

🔗 **Live Demo**: https://chatbot-aykhziasddpumss5ksjaof.streamlit.app/

---

## Features

- 🤖 Multiple AI models (DeepSeek, GPT-4o mini, Claude, Llama, Gemini)
- 🧠 Full conversation memory
- ⚙️ Customizable system prompt
- 🗑️ Clear chat anytime
- 🔑 Bring your own OpenRouter API key

## Models Available

| Model | Provider |
|-------|----------|
| DeepSeek Chat v3 | DeepSeek |
| GPT-4o mini | OpenAI |
| Claude 3.5 Haiku | Anthropic |
| Llama 3.3 70B | Meta |
| Gemini Flash 2.0 | Google |

## Run Locally

```bash
git clone https://github.com/Sdb002/chatbot.git
cd chatbot
pip install -r requirements.txt
streamlit run chatbot_app.py
```

## Usage

1. Get a free API key from [openrouter.ai](https://openrouter.ai)
2. Paste it in the sidebar
3. Pick a model
4. Start chatting

## Tech Stack

- [Streamlit](https://streamlit.io) — UI
- [OpenRouter](https://openrouter.ai) — AI model gateway
- [OpenAI SDK](https://github.com/openai/openai-python) — API client
