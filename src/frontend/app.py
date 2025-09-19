from flask import Flask, render_template, request, jsonify
from src.backend.rag_retriever import Retriever
from src.backend.rag_generator import Generator

app = Flask(__name__)

retriever = Retriever()
generator = Generator()

# Disable caching for development
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def home():
    return render_template("chatbotUI.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        query = request.json.get("query", "")
        mode = request.json.get("mode", "concise")

        retrieved = retriever.retrieve(query, top_k=3, mode=mode)

        if not retrieved:
            return jsonify({"answer": "Sorry, I couldn't find relevant news for that query", "sources": []})

        answer = generator.generate(query, retrieved,  mode=mode)

        return jsonify({"answer": answer, "sources": retrieved})
    except Exception as e:
        return jsonify({"answer": f"An error occurred: {e}", "sources": []})

if __name__ == "__main__":
    app.run(debug=True)
