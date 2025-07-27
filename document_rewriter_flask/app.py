from flask import Flask, render_template, request, send_file
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import docx2txt
import PyPDF2
import tempfile

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
TONE_OPTIONS = ["Friendly", "Corporate", "Formal", "Persuasive", "Casual", "Simplified"]

def extract_text(file):
    ext = file.filename.split('.')[-1]
    if ext == 'txt':
        return file.read().decode("utf-8")
    elif ext == 'docx':
        return docx2txt.process(file)
    elif ext == 'pdf':
        pdf = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in pdf.pages])
    return ""

def rewrite_text(input_text, selected_tone):
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7, model="gpt-4")
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a professional writing assistant that rewrites text in a selected tone."),
        ("user", "Rewrite the following text in a {tone} tone:\n\n{text}")
    ])
    prompt = template.format_messages(tone=selected_tone, text=input_text)
    response = llm(prompt).content
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    original_text = rewritten_text = selected_tone = ""
    if request.method == 'POST':
        selected_tone = request.form.get('tone')
        text_input = request.form.get('text_input')
        uploaded_file = request.files.get('file')

        if uploaded_file and uploaded_file.filename != "":
            original_text = extract_text(uploaded_file)
        else:
            original_text = text_input

        if original_text.strip():
            rewritten_text = rewrite_text(original_text, selected_tone)

    return render_template("index.html", tones=TONE_OPTIONS, original=original_text,
                           rewritten=rewritten_text, selected_tone=selected_tone)

@app.route('/download', methods=['POST'])
def download():
    rewritten_text = request.form.get("rewritten_text", "")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w') as f:
        f.write(rewritten_text)
        temp_file_path = f.name
    return send_file(temp_file_path, as_attachment=True, download_name="rewritten_text.txt")

if __name__ == '__main__':
    app.run(debug=True)
