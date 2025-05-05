from flask import Flask, render_template, request, send_file, Response
from flask_cors import CORS
import google.generativeai as genai
import os
import whisper
from moviepy import VideoFileClip
import tempfile
from fpdf import FPDF
import fitz  # PyMuPDF
import re
from unidecode import unidecode
from googletrans import Translator
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Google Gemini API
genai.configure(api_key="AIzaSyA_2UDjUr5saU2z8jNEkTvhcVbjojlYazM")

# Whisper ASR model
whisper_model = whisper.load_model("base")

# Translator
translator = Translator()

def extract_audio(video_path):
    try:
        print(f"[DEBUG] Extracting audio from: {video_path}")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        audio_path = tempfile.mktemp(suffix=".wav")
        video = VideoFileClip(video_path)
        if video.audio is None:
            raise ValueError("No audio found in the video.")
        video.audio.write_audiofile(audio_path, codec="pcm_s16le")
        return audio_path
    except Exception as e:
        return f"Error extracting audio: {str(e)}"

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return str(e)

def transcribe_audio(audio_path):
    try:
        result = whisper_model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return str(e)

def translate_to_english(text):
    try:
        detected = translator.detect(text)
        if detected.lang != "en":
            translated = translator.translate(text, dest="en")
            return translated.text
        return text
    except Exception as e:
        return text  # fallback if translation fails

def extract_math_equations(text):
    math_pattern = r"\b([a-zA-Z0-9\+\-\*\/\=\(\)\^]+)\b"
    equations = re.findall(math_pattern, text)
    return equations

def summarize_text(text):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = (
            "You are an expert in summarizing and teaching advanced mathematical and technical content. "
            "Your task is to read the following lecture or text and produce a comprehensive, structured summary that:\n"
            "- Retains all key definitions, theorems, principles, and conceptual explanations\n"
            "- Clearly and correctly writes out mathematical equations, formulas, and expressions\n"
            "- Includes step-by-step derivations if presented\n"
            "- Organizes the summary into logical sections or bullet points\n\n"
            f"Lecture or Source Text:\n{text}\n\n"
            "Now produce a clear, informative, and technically precise summary:"
        )
        response = model.generate_content(prompt)
        return response.text.strip() if response else "Summary not available."
    except Exception as e:
        return str(e)

def generate_unique_mcqs(summary, num_questions=30, difficulty="medium"):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"""
        You are an AI tasked with generating informative and challenging multiple-choice questions (MCQs) from educational content.

        Summary:
        "{summary}"

        Generate up to {num_questions} unique MCQs of '{difficulty}' difficulty.

        Format:
        ## MCQ
        Question: ...
        A) ...
        B) ...
        C) ...
        D) ...
        Correct Answer: ...
        """
        response = model.generate_content(prompt)
        return response.text.strip() if response else "MCQs not available."
    except Exception as e:
        return str(e)

def parse_mcqs(mcq_text):
    mcqs_list = []
    current = {}
    lines = mcq_text.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Question:"):
            if current:
                mcqs_list.append(current)
            current = {'question': line.replace("Question:", "").strip(), 'options': []}
        elif line.startswith(("A)", "B)", "C)", "D)")):
            current['options'].append(line[3:].strip())
        elif line.startswith("Correct Answer:"):
            current['answer'] = line.replace("Correct Answer:", "").strip()
    if current:
        mcqs_list.append(current)
    return mcqs_list

def save_as_pdf(content, filename):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Smart Lecture Assistant", ln=True, align="C")
            self.ln(5)
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    ascii_content = unidecode(content)
    for line in ascii_content.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_path = os.path.join("uploads", filename)
    pdf.output(pdf_path)
    return pdf_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            return render_template("index.html", error="No file uploaded.")

        difficulty = request.form.get("difficulty", "medium")
        num_questions = int(request.form.get("num_questions", 15))

        os.makedirs("uploads", exist_ok=True)
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join("uploads", filename)
        uploaded_file.save(file_path)

        if not os.path.exists(file_path):
            return render_template("index.html", error="File save failed.")

        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:
            audio_path = extract_audio(file_path)
            if isinstance(audio_path, str) and audio_path.startswith("Error"):
                return render_template("index.html", error=audio_path)
            text = transcribe_audio(audio_path)

        if not text:
            return render_template("index.html", error="Failed to extract content.")

        text = translate_to_english(text)
        math_equations = extract_math_equations(text)
        summary = summarize_text(text)
        mcqs_raw = generate_unique_mcqs(summary, num_questions, difficulty)
        mcqs_parsed = parse_mcqs(mcqs_raw)

        with open("uploads/summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        with open("uploads/mcqs.txt", "w", encoding="utf-8") as f:
            f.write(mcqs_raw)

        save_as_pdf(summary, "summary.pdf")
        save_as_pdf(mcqs_raw, "mcqs.pdf")

        return render_template("results.html", summary=summary, mcqs=mcqs_parsed, enumerate=enumerate, math_equations=math_equations)

    return render_template("index.html")

@app.route("/download/summary/txt")
def download_summary_txt():
    with open("uploads/summary.txt", "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, mimetype="text/plain; charset=utf-8", headers={"Content-Disposition": "attachment; filename=summary.txt"})

@app.route("/download/summary/pdf")
def download_summary_pdf():
    return send_file("uploads/summary.pdf", as_attachment=True)

@app.route("/download/mcqs/txt")
def download_mcqs_txt():
    with open("uploads/mcqs.txt", "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, mimetype="text/plain; charset=utf-8", headers={"Content-Disposition": "attachment; filename=mcqs.txt"})

@app.route("/download/mcqs/pdf")
def download_mcqs_pdf():
    return send_file("uploads/mcqs.pdf", as_attachment=True)

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
