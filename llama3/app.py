from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3_finance"
EXIT_KEYWORDS = ["退出", "再见", "结束", "bye"]

def query_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "发生错误")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    if any(k in user_input.lower() for k in EXIT_KEYWORDS):
        return jsonify({"response": "感谢使用，再见！", "exit": True})

    ai_response = query_ollama(user_input)
    return jsonify({"response": ai_response, "exit": False})

if __name__ == "__main__":
    app.run(debug=True)
