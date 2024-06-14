import os
import fitz  # PyMuPDF

# 1. Indexing documents
def index_documents(directory):
    indexed_documents = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                indexed_documents[filename] = file.read()
        elif filename.endswith(".pdf"):
            doc = fitz.open(os.path.join(directory, filename))
            text = ""
            for page in doc:
                text += page.get_text()
            indexed_documents[filename] = text
    return indexed_documents

# 2. Search function
def search_documents(indexed_documents, query):
    results = {}
    for filename, content in indexed_documents.items():
        relevance_score = 0
        words = content.split()
        for word in query.split():
            relevance_score += words.count(word)
        results[filename] = relevance_score
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return sorted_results


from transformers import pipeline

hypothesis_generator = pipeline("text-generation", model="gpt2", max_new_tokens=50)


# Rest of the Flask app remains the same...
# 3. Web interface (using Flask)
from flask import Flask, request, render_template, send_file
import os

# Function to retrieve file content
def get_file_content(filename):
    file_path = os.path.join("D:\Data Breast Cancer", filename)
    if filename.endswith(".txt"):
        with open(file_path, "r") as file:
            content = file.read()
    elif filename.endswith(".pdf"):
        doc = fitz.open(file_path)
        content = ""
        for page in doc:
            content += page.get_text()
    else:
        content = "Unsupported file format"
    return content


def get_file_path(filename):
    return os.path.join("D:\Data Breast Cancer", filename)

# Function to generate summary of the document using TextRank algorithm
from Sum2 import generate_summary
#from Hypo import generate_hypotheses
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    results = search_documents(indexed_documents, query)
    return render_template("results.html", results=results)

@app.route("/file/<filename>")
def get_file(filename):
    file_path = get_file_path(filename)
    if filename.endswith(".pdf"):
        return send_file(file_path, as_attachment=False)
    else:
        with open(file_path, "r") as file:
            content = file.read()
        return render_template("file_display.html", filename=filename, file_content=content)


@app.route("/summary/<filename>")
def get_summary(filename):
    content = get_file_content(filename)
    summary = generate_summary(content)
    return render_template("summary.html", filename=filename, summary=summary)

@app.route("/hypothesis/<filename>")
def get_hypotheses(filename):
    content = get_file_content(filename)
    hypotheses = generate_summary(content)
    return render_template("Hypo.html", filename=filename, hypotheses=hypotheses)

# Function to generate hypotheses using GPT-2 language model
"""def generate_hypotheses(content):
    hypotheses = hypothesis_generator(content, max_length=50, num_return_sequences=2, temperature=1.0)
    hypotheses_text = [hypothesis['generated_text'].strip() for hypothesis in hypotheses]
    return hypotheses_text

# Route to handle form submission for generating hypotheses
@app.route("/generate_hypotheses", methods=["POST"])
def generate_hypotheses_route():
    filename = request.form.get("filename")
    content = get_file_content(filename)
    hypotheses = generate_hypotheses(content)
    return render_template("Hypo.html", filename=filename, hypotheses=hypotheses)"""



if __name__ == "__main__":
    root = "D:\Data Breast Cancer"
    indexed_documents = index_documents(root)
    app.run(debug=True)
