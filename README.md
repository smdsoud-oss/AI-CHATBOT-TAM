# 🤖 TAM — Thoughtful Adaptive Mind

> **Your Personal AI Assistant** — Built from scratch by Mohammed Soud S N

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Railway-purple?style=for-the-badge)](https://web-production-31485.up.railway.app)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285f4?style=for-the-badge&logo=google)](https://ai.google.dev)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)](https://groq.com)

---

## 🌟 Live Demo

🔗 **Try TAM here:** [https://web-production-31485.up.railway.app](https://web-production-31485.up.railway.app)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Dual AI Engine** | Google Gemini + Groq with auto-fallback |
| 🎤 **Voice Input** | Speak to TAM using Web Speech API |
| 🔊 **Voice Output** | TAM speaks back in female voice |
| 🌐 **Live Web Search** | Real-time search via Tavily API |
| 📄 **File Reading** | Upload PDF, Word, Excel, CSV, PowerPoint |
| 🔢 **Math Solver** | Solves equations using SymPy |
| 🧠 **Critical Thinking** | Logic puzzles and argument analysis |
| 💻 **Code Generation** | Write, explain and debug code |
| 📚 **Personal Knowledge Base** | TAM knows about Soud's projects & skills |
| ⚡ **Streaming Responses** | Word-by-word like ChatGPT |
| 🌙 **Dark/Light Mode** | Toggle between themes |
| 📋 **Copy Button** | Copy any response or code block |
| 🔐 **Admin Panel** | Password-protected knowledge management |
| 📱 **Mobile Friendly** | Works on phones and tablets |

---

## 🏗️ Tech Stack

### Backend
- **Python 3.13** — Core language
- **Flask** — Web framework
- **Gunicorn** — Production server
- **Google Gemini API** — Primary AI (gemini-flash)
- **Groq API** — Backup AI (llama, mixtral models)
- **Tavily API** — Live web search
- **SymPy** — Math equation solver
- **SQLite** — Knowledge base storage

### File Processing
- **PyMuPDF** — PDF reading
- **python-docx** — Word documents
- **openpyxl** — Excel files
- **python-pptx** — PowerPoint slides
- **pandas** — CSV data analysis

### Frontend
- **HTML5 + CSS3** — Structure & styling
- **Vanilla JavaScript** — Chat logic & streaming
- **Web Speech API** — Voice input/output
- **Marked.js** — Markdown rendering

### Deployment
- **GitHub** — Version control
- **Railway.app** — Cloud hosting

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- API Keys: Groq, Gemini, Tavily



AI-CHATBOT-TAM/
├── src/
│ ├── chatbot.py # AI brain & routing logic
│ ├── math_solver.py # Math equation solver
│ ├── critical_thinking.py # Logic & reasoning engine
│ ├── web_search.py # Live web search
│ ├── pdf_reader.py # Multi-format file reader
│ ├── knowledge.py # Personal knowledge base
│ └── api_manager.py # AI fallback manager
├── templates/
│ ├── index.html # Main chat UI
│ ├── admin.html # Knowledge admin panel
│ └── admin_login.html # Admin login page
├── app.py # Flask web server
├── Procfile # Railway deployment
├── railway.json # Railway config
└── requirements.txt # Dependencies


---

## 🎯 How It Works

User Message
↓
Flask Server (app.py)
↓
TAM Router (chatbot.py)
↓
┌─────────────────────────────┐
│ Math? → SymPy Solver │
│ Logic? → Critical Thinking │
│ Current info? → Tavily │
│ File question? → Reader │
│ About Soud? → Knowledge DB │
│ General? → Gemini/Groq AI │
└─────────────────────────────┘
↓
Streaming Response → User



---

## 🔐 Admin Panel

Access at `/admin` to manage TAM's knowledge base:
- Upload files (PDF, Word, Excel, PPT)
- Add manual facts about yourself
- Delete individual knowledge items
- Password protected

---

## 👤 About the Developer

**Mohammed Soud S N (SMS)**
- 🎓 B.Tech in AI & Data Science (Pre-final year)
- 📍 Vaniyambadi, Tamil Nadu, India
- 🔗 [LinkedIn](https://www.linkedin.com/in/mohammed-soud-sn-313993347)
- 🤖 [Try TAM](https://web-production-31485.up.railway.app)

---

## 📊 What I Learned Building TAM

- Full-stack AI application development
- REST API design with Flask
- LLM integration (Gemini & Groq)
- Prompt engineering
- Real-time streaming responses
- Voice API integration
- Multi-format file processing
- Database management (SQLite)
- Cloud deployment (Railway + GitHub CI/CD)
- Mobile-responsive UI design

---

## 🌟 Star This Repo!

If you found TAM interesting, please ⭐ star this repository!

---

*Built with  by Mohammed Soud S N*
