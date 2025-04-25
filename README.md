# 🤖 DuoBot — A Dual-Mode AI Chatbot

**DuoBot** is a smart chatbot interface built with **Streamlit**, capable of switching between two powerful modes:

- 🧠 **Offline Mode** — Uses the **Mistral** language model via `ollama`, running fully local without internet.
- 🌐 **Online Mode** — Uses the **DuckDuckGo Search API** to fetch real-time web search results.

🎙️ It also includes **voice input**, 🖼️ image upload support, 🎨 pastel-themed UI, and 💾 local chat history session storage!

---

## 🌟 Screenshot

![DuoBot Screenshot]("C:\Users\snpoo\OneDrive\Desktop\dubot image.jpg")

---

## 🌐 Deployed App

You can try out the deployed version of DuoBot here:

[**DuoBot Streamlit App**](your-deployed-app-link)

---

## 🔘 Mode Selector

In the **sidebar**, you'll find a **dropdown** (referred to as the "dot") that lets you choose between:

- **Offline Mode** – Chat with the local model (Mistral via Ollama)
- **Online Mode** – Search the web using DuckDuckGo API

This dot-like dropdown is the heart of DuoBot’s **dual-mode design**.

---

## ✨ Features

- ✅ Dropdown mode selector: Offline (Mistral via Ollama) / Online (DuckDuckGo Search)
- 🎤 Voice input using `speechrecognition`
- 🖼️ Image upload support
- 💾 Chat history saved per session (like ChatGPT)
- 🎨 Stylish pastel UI with modern layout
- 📱 Bottom-up chat flow
- 🪄 Central welcome screen when idle
- 🔐 Local-only processing in offline mode

---

## 🛠️ Tech Stack

- Python 3.9+
- Streamlit
- Ollama (for local Mistral LLM)
- Mistral language model
- DuckDuckGo Search API
- SpeechRecognition + PyAudio
- JSON for local chat history

---

### 🎉 Contribute

Feel free to fork the project and submit pull requests! Here are a few ways you can contribute:

- Report bugs
- Add features (like more modes or different voice recognition options)
- Improve documentation

To contribute:

1. Fork the repository.
2. Clone your fork locally.
3. Create a new branch.
4. Implement your feature or fix.
5. Open a pull request!

---

### ✨ Acknowledgements

- **Streamlit** – For making it so easy to create beautiful web apps.
- **Ollama** – For providing local large language models.
- **DuckDuckGo** – For their reliable search API.
- **SpeechRecognition** – For enabling voice input.
- **PyAudio** – For handling audio recording.

---

### 🪪 License

This project is licensed under the [MIT License](LICENSE).

---

### 🌟 Star This Repo

If you like this project, please consider starring it on GitHub ⭐. Your support helps a lot!

---

### ✨ Made with ❤️ by Poojitha, lakshmi bhavani
