📚 Smart Lecture Assistant
Smart Lecture Assistant is a Flask-based web application that allows users to upload educational videos or PDFs and automatically generate:

📄 A structured summary of the content

❓ Multiple-choice questions (MCQs)

➗ Extracted math equations

📥 Downloadable TXT and PDF formats

Built with advanced AI tools like Whisper, Google Gemini, and Google Translate, this tool is ideal for students, educators, and content creators seeking quick educational content generation.

🔧 Features
🎥 Video Support: Extracts audio from educational videos and transcribes them using Whisper.

📄 PDF Support: Parses text directly from uploaded PDFs.

🌐 Language Support: Detects and translates non-English text to English.

🧠 AI-Powered Summarization: Uses Google Gemini to summarize lectures in a clean and structured format.

📝 MCQ Generation: Generates unique, difficulty-based MCQs from the summary.

🧮 Equation Extraction: Finds and lists math equations.

📤 Downloadable Outputs: Summary and MCQs can be downloaded in TXT and PDF formats.

🧪 Dependencies
Flask

Flask-CORS

Whisper (OpenAI)

moviepy

PyMuPDF (fitz)

FPDF

googletrans

google-generativeai

unidecode

📌 Notes
Only supports .pdf, .mp4, and .mkv files.

Whisper model is set to "base" for faster performance.

Outputs are saved in the uploads/ directory.

🤝 Acknowledgements
OpenAI Whisper

Google Generative AI

moviepy

PyMuPDF

FPDF
