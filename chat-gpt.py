import openai
from openai import OpenAI

# Initialize client with API key
client = OpenAI(api_key="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")  # replace with your actual API key

response = client.chat.completions.create(
    model="gpt-4o-mini",  # or "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a fun fact about space."}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
