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
        "你要扮演一位名叫邵奕涵的大二学生。一些信息如下"
        "你就读于浙江大学数学系，你的MBTI是 INTP，喜欢躺平。"
        "你来自浙江温州，是一位女生，爱好是吃喝玩乐。"
        "在回答问题时，你应该以‘我’的第一人称回答，而不是称呼自己为‘邵奕涵’。"
        "如果有人问你的个人信息，你可以回答你的背景信息。"
        "如果有人问一些难以回答的内容，你可以说‘我咋知道’。"
        "如果有人问你数学问题，你可以说“你自己没脑子吗？”，或者这样类似的攻击性的话语"
        "你说话要稍微简短些，口语化一些，不要太礼貌，带一点攻击性"
        "接下来，聊天正式开始，在第一轮对话中，不管对方说什么，你先说：“你好，我是邵奕涵”"
        
    )
}

app = Flask(__name__)

messages = [system_message]

@app.route("/")
def index():
    return render_template("index_robot21.html")


    

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

# 新的 API 路由，用于根据对话生成推荐书单
@app.route("/generate_books", methods=["GET"])
def generate_books():
    try:
        # 从历史对话中获取对话内容，生成书单
        max_length = 1000  # 限制对话内容的长度
        conversation_text = "\n".join([msg["content"] for msg in messages if msg["role"] == "user"])[-max_length:]

        # 提示 GPT 生成书籍
        prompt = (
            f"根据以下对话内容，生成三本虚构的中文书籍推荐（幽默、文艺一些），并包含书名、作者和类别。其中作者不能虚构\n"
            f"对话内容：\n{conversation_text}\n\n"
            f"请严格按照以下 JSON 格式返回：\n"
            f'[{{"book_id": 1, "title": "书名1", "author": "作者1", "genre": "类别1"}},'
            f'{{"book_id": 2, "title": "书名2", "author": "作者2", "genre": "类别2"}},'
            f'{{"book_id": 3, "title": "书名3", "author": "作者3", "genre": "类别3"}}]'
        )

        # 调用 GPT-3 来生成书单
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        ai_reply = response.choices[0].message.content
        print(f"GPT 返回内容: {ai_reply}")  # 调试日志

        # 解析生成的书籍清单
        import json
        try:
            # 移除可能的代码块标记符
            if ai_reply.startswith("```json"):
                ai_reply = ai_reply[7:]
            if ai_reply.endswith("```"):
                ai_reply = ai_reply[:-3]

            book_list = json.loads(ai_reply.strip())  # 使用 json.loads 解析
            print(f"解析后的书单: {book_list}")  # 调试日志
            return jsonify({"books": book_list})
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            return jsonify({"error": "无法解析生成的书籍列表"}), 500

    except Exception as e:
        print(f"API 调用失败: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
