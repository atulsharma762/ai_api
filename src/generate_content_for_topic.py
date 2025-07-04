from utils.database import Database
from utils.chatgpt import ChatGPTClient

obj_ai=ChatGPTClient()
obj_db = Database()
course_name="Swift"

topic_list = [
    "Introduction to Swift"
  ]

for topic in topic_list:
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

