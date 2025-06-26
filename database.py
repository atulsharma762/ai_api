# database.py
import mysql.connector
import os, json
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ Database connection successful.")
        except mysql.connector.Error as err:
            print(f"❌ Database connection failed: {err}")
            raise

    # Insert data into any table
    def insert(self, table: str, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"✅ Inserted into {table}.")

    # Select rows with optional condition
    def select(self, table: str, where: str = None, values: tuple = None):
        query = f"SELECT * FROM {table}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()

    # Update rows based on a condition
    def update(self, table: str, data: dict, where: str, values: tuple):
        set_clause = ", ".join([f"{key} = %s" for key in data])
        update_values = tuple(data.values()) + values
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"
        self.cursor.execute(query, update_values)
        self.connection.commit()
        print(f"🔄 Updated {table}.")

    # Delete rows from a table
    def delete(self, table: str, where: str, values: tuple):
        query = f"DELETE FROM {table} WHERE {where}"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"🗑️ Deleted from {table}.")



    def upsert_topic_content(self, course_id, topic_name, topic_content):
        query = """
        INSERT INTO course_topic_details (course_id, topic_name, topic_content)
        VALUES (%s, %s, %s)
        ON CONFLICT (course_id, topic_name) DO UPDATE SET topic_content = EXCLUDED.topic_content;
        """
        self.cursor.execute(query, (course_id, topic_name, topic_content))

    # def upsert_sub_topics(self, course_id, topic_name, topic_content, sub_topics_to_covered):
    #     try:
    #         query = """
    #         INSERT INTO course_topic_details (course_id, topic_name, topic_content, sub_topics_to_covered)
    #         VALUES (%s, %s, %s)
    #         ON DUPLICATE KEY UPDATE topic_content = VALUES(topic_content);
    #         """
    #         self.cursor.execute(query, (course_id, topic_name, topic_content,sub_topics_to_covered))
    #         affected = self.cursor.rowcount
    #         if affected == 1:
    #             print("Inserted new row.")
    #         elif affected == 2:
    #             print("Updated existing row.")
    #         else:
    #             print("No change (data may already be the same).")
    #     except Exception as err:
    #         print(f"Query failed: {err}")
    #         raise

    def upsert_sub_topics(self, course_id, topic_name, topic_content, sub_topics_to_covered):
        try:
            sub_topics_to_covered = json.dumps(sub_topics_to_covered)

            query = """
            INSERT INTO course_topic_details (course_id, topic_name, topic_content, sub_topics_to_covered)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE topic_content = VALUES(topic_content),
                                    sub_topics_to_covered = VALUES(sub_topics_to_covered);
            """
            self.cursor.execute(query, (course_id, topic_name, topic_content, sub_topics_to_covered))
            affected = self.cursor.rowcount
            if affected == 1:
                print("Inserted new row.")
            elif affected == 2:
                print("Updated existing row.")
            else:
                print("No change (data may already be the same).")
        except Exception as err:
            print(f"Query failed: {err}")
            raise

    # Run any custom query
    def run_query(self, query: str, values: tuple = None):
        self.cursor.execute(query, values or ())
        if query.strip().upper().startswith("SELECT"):
            return self.cursor.fetchall()
        else:
            self.connection.commit()
            return self.cursor.rowcount

    # Close the connection
    def close(self):
        self.cursor.close()
        self.connection.close()
        print("🔒 Database connection closed.")
