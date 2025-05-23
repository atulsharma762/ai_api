import openai
from openai import OpenAI

# Initialize client with API key

response = client.chat.completions.create(
    model="gpt-4o-mini",  # or "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a fun fact about space."}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
