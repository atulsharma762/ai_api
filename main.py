import json

from database import Database
from chatgpt import ChatGPTClient

str_topic="Kotlin Basics"
obj_ai=ChatGPTClient()
obj_db = Database()
course_name="API Automation"

topic_list = [
    "API Automation using Java",
    "API Automation using Python"
]


for topic in topic_list:
    # if topic!='Web Element Interactions':
    #     continue
    print(f"updating for {topic}")
    response = obj_ai.get_topic_content(topic, course_name)
    response=obj_ai.extract_json(response)
    # response=response.replace('```json','').replace('```','')
    obj_db.update(
        "course_topic_details",
        {"topic_content": response},
        "topic_name = %s",
        (topic,)
    )
    print("updated...")

