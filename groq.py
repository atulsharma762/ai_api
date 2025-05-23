import requests

headers = {
    "Authorization": "",
    "Content-Type": "application/json",
}

data = {
    "model": "llama3-8b-8192",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Give me a tweet, announcing results between Nagal vs Federer, use icons, add date"}
    ]
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
print(response.json()["choices"][0]["message"]["content"])
