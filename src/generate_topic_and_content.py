import json

from utils.database import Database
from utils.chatgpt import ChatGPTClient
import pandas as pd

df = pd.read_csv('../inputs/topic_list.csv')
yes_topics = df[df['yes_no'] == 'yes']

obj_ai=ChatGPTClient()
obj_db = Database()

topic_list=[]


def convert_to_json(topic_list):
    try:
        topic_list_json = json.loads(topic_list)
        return topic_list_json
    except Exception as e:
        print(str(e))
        return topic_list

for index, row in df.iterrows():
    course_id = row['course_id']
    course_name = row['course_name']
    yes_no = row['yes_no']
    if yes_no=='yes':
        print(f"{course_id}. {course_name} (Selected: {yes_no})")
        topic_list=obj_ai.get_topic_list(course_name)
        topic_list_json=convert_to_json(topic_list)
        print(topic_list)
        topic_order_id=1
        topic_length=len(topic_list_json)
        print(f"Total Topics: {len(topic_list_json)}")
        for dict_sub_topic in topic_list_json:
                print(f"topic_order_id={topic_order_id}/{topic_length}/{course_name}")
                topic_content = obj_ai.get_topic_content_specific(dict_sub_topic['sub_topic_name'], course_name, dict_sub_topic['sub_topics_to_covered'])
                obj_db.upsert_sub_topics(course_id, dict_sub_topic['sub_topic_name'],topic_content, dict_sub_topic['sub_topics_to_covered'], topic_order_id)
                topic_order_id = topic_order_id+1



