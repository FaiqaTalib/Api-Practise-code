import os
from flask import Flask, render_template, request
from your_summarizer_module import summarize_file
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------
# Load API Key
# ---------------------------
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyBqWaQRW9rkGVVBQ_JQp7XdC-oJEmVhErE"))

# ---------------------------
# Initialize Gemini Model
# ---------------------------
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_response(prompt):
    """Chatbot response generator"""
    response = model.generate_content(prompt)
    return response.text


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------------------
# Home Page
# ---------------------------
@app.route("/")
def home():
    return render_template("file.html")

# ---------------------------
# File Summarizer
# ---------------------------
@app.route("/index", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        if 'file' not in request.files:
            summary = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                summary = "No file selected"
            else:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                summary = summarize_file(file_path)

    return render_template("index.html", summary=summary)

# ---------------------------
# Chatbot Route
# ---------------------------
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    user_input = None
    answer = None

    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            answer = generate_response(user_input)

    return render_template("chat.html", user_input=user_input, answer=answer)


# ---------------------------
# Run Server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
