import requests
import json

# 访问 Ollama API
def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {"model": "mistral", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # 检查 HTTP 请求是否成功
        return response.json().get("response", "未返回有效响应")
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"

# 主函数
def main():
    print("欢迎使用 AI 代理！输入 '退出', 'bye', 或 'q' 以退出程序。")
    while True:
        user_input = input("你: ").strip()
        if not user_input:
            print("输入不能为空，请重新输入。")
            continue
        if user_input.lower() in ["退出", "bye", "q"]:
            print("再见！")
            break
        response = query_ollama(user_input)
        print("AI:", response)

if __name__ == "__main__":
    main()