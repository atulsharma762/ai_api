from io import StringIO
from typing import TextIO
import pandas as pd
import json
from io import StringIO
from utils.database import Database
from utils.chatgpt import ChatGPTClient
import pandas as pd


obj_ai=ChatGPTClient()
obj_db = Database()



def convert_to_json(topic_list):
    try:
        topic_list_json = json.loads(topic_list)
        return topic_list_json
    except Exception as e:
        print(str(e))
        return topic_list

blog_titles=[f"The Unspoken Costs of Choosing the “Wrong” Programming Language"]
# blog_titles=["Why Prompt Engineering Is a Temporary Skill",'The Unspoken Costs of Choosing the “Wrong” Programming Language','When Not to Refactor: The Ethics of Leaving Bad Code Alone'
#             'If Copilot Writes 80% of the Code, What Should You Focus On?']
for topic_name in blog_titles:
    quiz_content = obj_ai.get_blog_content(topic_name)
    obj_db.upsert_blog(topic_name,quiz_content)
# topic_order_id = topic_order_id+1



