from io import StringIO
from typing import TextIO
import pandas as pd
import json
from datetime import datetime

from utils.database import Database
from utils.chatgpt import ChatGPTClient

# Load the Excel file
input_path = '../inputs/quiz_category.xlsx'
category_df = pd.read_excel(input_path)

# Filter rows marked 'yes'
selected_categories = category_df[category_df['yes_no'].str.lower() == 'yes']

# Initialize helper classes
chatgpt_client = ChatGPTClient()
db_client = Database()

# Get today's date
today_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def convert_to_json(data: str):
    try:
        return json.loads(data)
    except Exception as e:
        print(f"JSON parsing error: {e}")
        return data

def fetch_ques_count(course_name):
    try:
        count_query = "SELECT COUNT(*) as row_count FROM quiz WHERE course_name = %s"
        db_client.cursor.execute(count_query, (course_name,))
        result = db_client.cursor.fetchone()
        record_count = result['row_count'] if result else 0
        print(f"✅ Total questions for '{course_name}' = {record_count}")
        return record_count
    except Exception as e:
        print(f"❌ Error fetching count for '{course_name}': {e}")
        return 0  # Or return None if you want to signal failure


# Iterate through the filtered DataFrame
for index, row in selected_categories.iterrows():
    category_id = row['category_id']
    category = row['category']
    sub_category = row['sub_category']

    print(f"{category_id}. {category} (Selected: {sub_category})")

    topic_name = f"{category}-{sub_category}"

    try:
        quiz_csv_data = chatgpt_client.get_quiz_list(category, sub_category, 50)
        csv_file: TextIO = StringIO(quiz_csv_data)
        quiz_df = pd.read_csv(csv_file, quotechar='"', on_bad_lines='skip')

        db_client.upsert_quiz(quiz_df)

        # ✅ Update status and updated_at in the original DataFrame
        category_df.at[index, 'yes_no'] = 'no'
        category_df.at[index, 'status'] = 'Done'
        category_df.at[index, 'updated_at'] = today_str
        category_df.at[index,'count']=fetch_ques_count(sub_category)

    except Exception as e:
        print(f"Error processing {topic_name}: {e}")
        category_df.at[index, 'count'] = str(e)
        continue

saved = False
max_retries = 3  # Optional: to avoid infinite loops
retry_count = 0

while not saved and retry_count < max_retries:
    try:
        category_df.to_excel(input_path, index=False)
        print("\n✅ Excel file saved successfully.")
        saved = True
    except PermissionError:
        print(f"\n❌ Cannot save '{input_path}'. It is currently open.")
        input("🔁 Please close the file in Excel and press Enter to retry...")
        retry_count += 1
    except Exception as e:
        print(f"\n❌ Unexpected error while saving Excel file: {e}")
        break
