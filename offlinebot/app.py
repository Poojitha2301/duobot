import streamlit as st
import datetime
import json
import os
import subprocess
import speech_recognition as sr
from duckduckgo_search import DDGS

st.set_page_config(page_title="DuoBot", layout="wide")

HISTORY_FILE = "chat_history.json"

# ---------- Load & Save Chat History ----------
def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_chat_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)

# ---------- Model Handlers ----------
def run_local_model(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        return result.stdout.decode("utf-8") if result.returncode == 0 else f"⚠️ Error: {result.stderr.decode('utf-8')}"
    except subprocess.TimeoutExpired:
        return "⏱️ Error: Mistral model timed out."

def search_and_respond(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "🔍 No relevant information found online."
        return "\n\n".join(f"**[{r['title']}]({r['href']})**: {r['body']}" for r in results)
    except Exception as e:
        return f"❌ Error accessing DuckDuckGo: {str(e)}"

# ---------- Voice Input ----------
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Listening... Speak now.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"✅ Recognized: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("😕 Could not understand audio.")
        return ""
    except sr.RequestError as e:
        st.error(f"🔌 API error: {e}")
        return ""

# ---------- Session Initialization ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.messages = []

chat_history = load_chat_history()
current_session_id = st.session_state.session_id
if current_session_id not in chat_history:
    chat_history[current_session_id] = []
    save_chat_history(chat_history)

# ---------- Sidebar ----------
with st.sidebar:
    st.image(r"C:\Users\snpoo\OneDrive\Desktop\bot image.jpg", width=50)
    st.title("🤖 DuoBot")
    mode = st.selectbox("Choose Mode", ["Offline", "Online"])
    uploaded_image = st.file_uploader("Upload image (optional)", type=["jpg", "jpeg", "png"])

    if st.button("➕ New Chat"):
        st.session_state.session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        st.session_state.messages = []

    if st.button("🧹 Clear Current Chat"):
        st.session_state.messages = []
        chat_history[st.session_state.session_id] = []
        save_chat_history(chat_history)

    st.markdown("### 📂 Sessions")
    for sid in sorted(chat_history.keys(), reverse=True):
        label = f"Session {sid[-6:]}"
        if st.button(label, key=sid):
            st.session_state.session_id = sid
            st.session_state.messages = chat_history.get(sid, [])

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        .user-msg {
            background-color: #d1ecf1;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 80%;
            align-self: flex-end;
        }
        .bot-msg {
            background-color: #cce5ff;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 80%;
            align-self: flex-start;
        }
        .chat-container {
            display: flex;
            flex-direction: column-reverse;
            height: 70vh;
            overflow-y: auto;
            background-color: #fff9ed;
            padding: 1rem;
            border-radius: 8px;
        }
        .welcome-container {
            height: 70vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #fff9ed;
            padding: 2rem;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Main Chat Area ----------
if st.session_state.messages:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role_class = 'user-msg' if msg["role"] == "user" else 'bot-msg'
        st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="welcome-container">
            <div>
                <h3>👋 Welcome to DuoBot!</h3>
                <p>I'm a dual-mode AI chatbot that works <strong>offline</strong> using a local model (Mistral) or <strong>online</strong> using DuckDuckGo search.</p>
                <p>💡 Select a mode and ask me anything!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---------- Voice Input ----------
if st.button("🎤 Use Voice Input"):
    voice_text = recognize_speech()
    if voice_text:
        st.session_state.messages.append({"role": "user", "content": voice_text})
        with st.spinner("Thinking..."):
            response = run_local_model(voice_text) if mode == "Offline" else search_and_respond(voice_text)
        st.session_state.messages.append({"role": "bot", "content": response})
        chat_history[st.session_state.session_id] = st.session_state.messages
        save_chat_history(chat_history)

# ---------- Text Input ----------
user_input = st.text_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = run_local_model(user_input) if mode == "Offline" else search_and_respond(user_input)
    st.session_state.messages.append({"role": "bot", "content": response})
    chat_history[st.session_state.session_id] = st.session_state.messages
    save_chat_history(chat_history)
