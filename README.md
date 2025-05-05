# Smart Lecture Assistant 🎓🤖

**An AI-powered multimodal framework for automatic lecture summarization, mathematical content interpretation, and assessment generation.**

---

## 🔍 Overview

Smart Lecture Assistant is a Flask-based web application that allows users to upload **video** or **PDF lecture files** and automatically generates:
- ✅ A comprehensive **summary**
- 🧮 Extracted **mathematical expressions**
- ❓ A set of unique, AI-generated **multiple-choice questions (MCQs)**

This tool is designed to assist students, educators, and self-learners in quickly digesting complex educational content.

---

## 🚀 Key Features

- 🎥 Accepts both **PDFs** and **video lectures**
- 🗣️ Uses **Whisper ASR** to transcribe speech from video/audio
- 🌐 Automatically **translates non-English content** to English
- 📚 Summarizes content using **Google Gemini Pro**
- 🧠 Extracts and preserves **mathematical equations**
- 📝 Generates **up to 30 MCQs** with customizable difficulty
- 📄 Supports **TXT and PDF downloads** of summary and questions

---

## 🛠️ Tech Stack

| Technology        | Purpose                                      |
|-------------------|----------------------------------------------|
| Flask             | Backend web framework                        |
| Google Gemini Pro | Summarization and MCQ generation             |
| OpenAI Whisper    | Audio transcription from video lectures      |
| PyMuPDF (`fitz`)  | PDF text extraction                          |
| Google Translate  | Multilingual support                         |
| FPDF              | PDF export of summary and MCQs               |
| HTML/CSS/JS       | Frontend rendering and interaction           |

---

## 📦 Dependencies
Flask

flask_cors

google-generativeai

openai-whisper

moviepy

fpdf

PyMuPDF

googletrans==4.0.0-rc1

unidecode

werkzeug

## 💡 Future Enhancements
📌 Flashcards and concept map generation

📊 Real-time quiz scoring

🌍 Multilingual support for summaries and questions

☁️ Cloud storage for files and results



