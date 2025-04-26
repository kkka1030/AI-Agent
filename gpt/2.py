import openai
from openai import OpenAI

# 设置 API Key
client = OpenAI(
            api_key="sk-CDdT0FyRDSWnUqhTqNbrg07mNGQZkKNOjI8epi8oRfQCcorE", # 替换为您的ZCHAT API密钥
            base_url="https://api.zchat.tech/v1"
        )

# 设定 AI 的角色
system_message = {
    "role": "system",
    "content": (
        "你是一位名叫庄博涵的教授，是人工智能领域的专家。"
        "你有深厚的技术背景，擅长机器学习、自然语言处理和深度学习。"
        "你说话专业、富有逻辑性，并能用通俗易懂的方式解释复杂的概念。"
        "如果有人问你个人信息，你可以告诉他们你在多个国际AI会议上发表过论文，"
        "并且你热爱分享 AI 知识，希望帮助更多人理解人工智能。"
    )
}
# 记录对话历史
messages = [system_message]


def chat_with_ai():
    print("欢迎使用 庄教授AI 聊天助手！输入 'exit' 退出。")
    while True:
        user_input = input("你: ")
        if user_input.lower() == "exit":
            print("再见！")
            break
        messages.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 或者使用 "gpt-3.5-turbo"
                messages=messages
            )
            ai_reply = response.choices[0].message.content
            print(f"庄博涵: {ai_reply}\n")
        except Exception as e:
            print("发生错误:", e)

# 运行聊天函数
if __name__ == "__main__":
    chat_with_ai()
