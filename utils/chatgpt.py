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
        prompt_text = self.load_prompt("../inputs/prompts/prompt.txt")
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
        prompt_text = self.load_prompt("../inputs/prompts/prompt_specific.txt")
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

    def get_interview_content_specific(self, topic_name: str = "Java", course_name: str="Java", sub_topic_list=None) -> str:
        print(f"fetching response for {topic_name}...")
        prompt_text = self.load_prompt("../inputs/prompt_specific_interview.txt")
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

    def get_coding_content_specific(self, topic_name: str = "Java", course_name: str="Java", sub_topic_list=None) -> str:
        print(f"fetching response for {topic_name}...")
        prompt_text = self.load_prompt("../inputs/prompts/prompt_specific_coding.txt")
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
            # Access message content correctly
            raw = response.choices[0].message.content.strip()

            # Strip markdown code fences if present
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.endswith("```"):
                raw = raw[:-3]

            parsed_json = json.loads(raw)
            return parsed_json
        except Exception as e:
            print(str(e))
            # As fallback, return the raw content instead of raising
            return response.choices[0].message.content

    def get_topic_list(self, topic_name: str = "Java") -> str:
        print("fetching response...")
        prompt_text = self.load_prompt("../inputs/prompts/prompt_topics.txt")
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

    def get_interview_topic_list(self, topic_name: str = "Java") -> str:
        print("fetching response...")
        prompt_text = self.load_prompt("../inputs/prompt_topics_interview.txt")
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

    def get_coding_topic_list(self, topic_name: str = "Java") -> str:
        print("fetching response...")
        prompt_text = self.load_prompt("../inputs/prompts/prompt_topics_coding_probs.txt")
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

    def get_quiz_list(self, category: str = "Programming", sub_category: str = "Java", category_id: int=1, ques_count: int= 10) -> str:
        print("fetching response...")
        prompt_text = self.load_prompt("../inputs/prompts/prompt_quiz.txt")
        prompt_text = prompt_text.replace("#category#", category)
        prompt_text = prompt_text.replace("#sub_category#", sub_category)
        prompt_text = prompt_text.replace("#ques_count#", str(ques_count))
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7
        )
        return self.extract_csv(response.choices[0].message.content)

    def get_blog_content(self, blog_title) -> str:
        print(f"fetching response...{blog_title}")
        prompt_text = self.load_prompt("../inputs/prompts/prompt_blog.txt")
        prompt_text = prompt_text.replace("#topic_name#", blog_title)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7
        )
        return self.extract_json(response.choices[0].message.content)


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

    def extract_csv(self, raw_response: str):
        """
        Extracts and parses JSON content from GPT responses,
        even if wrapped in ```json or ``` marks.
        """
        # Remove markdown code fences if present
        clean = re.sub(r"^```(?:csv)?\s*", "", raw_response.strip())
        clean = re.sub(r"\s*```$", "", clean)

        try:
            return clean
        except json.JSONDecodeError as e:
            print("❌ Failed to parse JSON:", e)
            print("📝 Response received:\n", clean)
            return raw_response

# if __name__ == "__main__":
#     chatgpt = ChatGPTClient(prompt_file_path="prompt.txt")
#     reply = chatgpt.get_response()
#     print(reply)
