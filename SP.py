import os

# 1. Indexing documents
def index_documents(directory):
    indexed_documents = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                indexed_documents[filename] = file.read()
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

# 3. Web interface (using Flask)
from flask import Flask, request, render_template
import os

# Function to retrieve file content
def get_file_content(filename):
    file_path = os.path.join("D:\DataSet", filename)
    with open(file_path, "r") as file:
        content = file.read()
    return content

# Function to generate summary of the document using TextRank algorithm
from Sum2 import generate_summary
from Hypo import generate_hypotheses
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
    content = get_file_content(filename)
    return render_template("file_display.html", filename=filename, file_content=content)

@app.route("/summary/<filename>")
def get_summary(filename):
    content = get_file_content(filename)
    summary = generate_summary(content)
    return render_template("summary.html", filename=filename, summary=summary)

@app.route("/hypothesis/<filename>")
def get_hypothesis(filename):
    content = get_file_content(filename)
    #hypothesis = generate_hypotheses(content)
    hypothesis = ["1jfksjff", "sjfijsginknbknh"]
    return render_template("Hypo.html", filename=filename, hypothesis=hypothesis)


if __name__ == "__main__":
    root = "D:\DataSet"
    indexed_documents = index_documents(root)
    app.run(debug=True)
