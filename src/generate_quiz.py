from io import StringIO
from typing import TextIO
import pandas as pd
import json
from io import StringIO
from utils.database import Database
from utils.chatgpt import ChatGPTClient
import pandas as pd

df = pd.read_csv('../inputs/quiz_category.csv')
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
    category_id = row['category_id']
    category = row['category']
    sub_category = row['sub_category']
    yes_no = row['yes_no']
    if yes_no=='yes':
        print(f"{category_id}. {category} (Selected: {sub_category})")
        topic_name=f"{category}-{sub_category}"
        quiz_content = obj_ai.get_quiz_list(category, sub_category, category_id, 100)
        # csv_file = StringIO(quiz_content)
        csv_file: TextIO = StringIO(quiz_content)

        df = pd.read_csv(csv_file, quotechar='"', on_bad_lines='skip')
        df['category']=category_id
        obj_db.upsert_quiz(df)
        # topic_order_id = topic_order_id+1



