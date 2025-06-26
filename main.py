import json

from database import Database
from chatgpt import ChatGPTClient

str_topic="Kotlin Basics"
obj_ai=ChatGPTClient()
obj_db = Database()
course_name="Python Selenium"
# topic_list = [
#     "Introduction to Selenium",
#     "Environment Setup",
#     "Selenium Commands",
#     "Web Element Interactions",
#     "Working with Forms",
#     "XPath and CSS Selectors",
#     "Synchronization in Selenium",
#     "Handling Alerts and Pop-ups",
#     "Working with Frames and Windows",
#     "Handling Web Tables",
#     "Mouse and Keyboard Actions",
#     "Taking Screenshots",
#     "Scrolling and JavaScript Execution",
#     "Handling File Uploads and Downloads",
#     "Selenium with Test Frameworks",
#     "Page Object Model (POM)",
#     "Data-Driven Testing",
#     "Headless Browser Testing",
#     "Advanced Topics",
#     "Best Practices in Selenium Automation"
# ]

topic_list = [
    "Working with Forms",
    "XPath and CSS Selectors",
    "Synchronization in Selenium",
    "Handling Alerts and Pop-ups",
    "Working with Frames and Windows",
    "Handling Web Tables",
    "Mouse and Keyboard Actions",
    "Taking Screenshots",
    "Scrolling and JavaScript Execution",
    "Handling File Uploads and Downloads",
    "Selenium with Test Frameworks",
    "Page Object Model (POM)",
    "Data-Driven Testing",
    "Headless Browser Testing",
    "Advanced Topics",
    "Best Practices in Selenium Automation"
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

