import openai
import os
from dotenv import load_dotenv
import json
import re


class ChatGPTClient:
    def __init__(self, prompt_file_path: str = "prompt.txt", model: str = "gpt-4o"):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)

    def load_prompt(self, file_path: str="prompt.txt") -> str:
        print("loading prompt...")
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def get_topic_content(self, topic_name: str = "Java", course_name: str= "Java", sub_topic_list=None) -> str:
        print("fetching response...")
        prompt_text = self.load_prompt("prompt.txt")
        prompt_text=prompt_text.replace("#topic_name#",topic_name)
        prompt_text = prompt_text.replace("#course_name#", course_name)
        prompt_text = prompt_text.replace("#course_name#", course_name)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    def get_topic_content_specific(self, topic_name: str = "Java", course_name: str="Java", sub_topic_list=None) -> str:
        print(f"fetching response for {topic_name}...")
        prompt_text = self.load_prompt("prompt_specific.txt")
        prompt_text=prompt_text.replace("#topic_name#",topic_name)
        prompt_text = prompt_text.replace("#course_name#", course_name)
        prompt_text = prompt_text.replace("#sub_topic_list#", str(sub_topic_list))
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7
        )
        return self.parse_content(response)

    def parse_content(self, response):
        try:
            raw = response['choices'][0]['message']['content'].strip()
            if raw.startswith("```json"):
                raw = raw[7:]  # remove ```json
            if raw.endswith("```"):
                raw = raw[:-3]  # remove ```

            parsed_json = json.loads(raw)
            return parsed_json
        except Exception as e:
            print(str(e))
            return response['choices'][0]['message']['content']

    def get_topic_list(self, topic_name: str = "Java") -> str:
        print("fetching response...")
        prompt_text = self.load_prompt("prompt_topics.txt")
        prompt_text = prompt_text.replace("#topic_name#", topic_name)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    def extract_json(self, raw_response: str):
        """
        Extracts and parses JSON content from GPT responses,
        even if wrapped in ```json or ``` marks.
        """
        # Remove markdown code fences if present
        clean = re.sub(r"^```(?:json)?\s*", "", raw_response.strip())
        clean = re.sub(r"\s*```$", "", clean)

        try:
            return clean
        except json.JSONDecodeError as e:
            print("❌ Failed to parse JSON:", e)
            print("📝 Response received:\n", clean)
            return None


# if __name__ == "__main__":
#     chatgpt = ChatGPTClient(prompt_file_path="prompt.txt")
#     reply = chatgpt.get_response()
#     print(reply)
