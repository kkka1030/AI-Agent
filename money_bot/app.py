from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import json

# 设置 OpenAI API Key
client = OpenAI(
    api_key="sk-CDdT0FyRDSWnUqhTqNbrg07mNGQZkKNOjI8epi8oRfQCcorE",  # 替换为你的 API Key
    base_url="https://api.zchat.tech/v1"
)

# 设定 AI 的角色
system_message = {
    "role": "system",
    "content": (
        "你是一名基金投资助手，用于给新人投资者提供投资基金的建议"
        
    )
}

app = Flask(__name__)

messages = [system_message]

@app.route("/")
def index():
    return render_template("index.html")


    

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "输入内容不能为空"}), 400

    messages.append({"role": "user", "content": user_message})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 也可以使用 "gpt-4"（如果你的 API 支持）
            messages=messages
        )

        ai_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_reply})

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
