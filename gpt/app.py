from flask import Flask, render_template, request, jsonify
from openai import OpenAI

# 设置 OpenAI API Key
client = OpenAI(
    api_key="",  # 替换为你的 API Key
    base_url=""
)

# 设定 AI 的角色
system_message = {
    "role": "system",
    "content": (
        "你是一位名叫庄博涵的教授，是人工智能领域的专家。"
        "你有深厚的技术背景，擅长机器学习、自然语言处理和深度学习。"
        "你是东北人，热情开朗，爱唠嗑。"
        "如果有人问你个人信息，你可以告诉他们你在多个国际AI会议上发表过论文，"
        "你很喜欢护手霜，每天都会用很多次"
    )
}

app = Flask(__name__)

# 记录对话历史
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
    app.run(debug=True)
