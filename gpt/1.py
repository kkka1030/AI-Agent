from openai import OpenAI

def chat_completion_example():
    try:
        # 创建聊天完成请求
        client = OpenAI(
            api_key="", # 
            base_url=""
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "developer", "content": "你是一个有帮助的助手。"},
                {
                    "role": "user",
                    "content": "你好，请介绍一下自己。",
                },
            ],
        )
        # 打印响应
        print("Assistant:", response.choices[0].message.content)

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    print("=== 聊天完成示例 ===")
    chat_completion_example()
