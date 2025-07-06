import mysql.connector
import os

def stream_users_in_batches(batch_size):
    """Generator: fetch user_data in batches of size batch_size"""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("MYSQL_PASSWORD"),    # Set your MySQL password here
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM user_data")
    total_rows = cursor.fetchone()['count']

    for offset in range(0, total_rows, batch_size):
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        batch = cursor.fetchall()
        if batch:
            yield batch

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """Process each batch: print users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
