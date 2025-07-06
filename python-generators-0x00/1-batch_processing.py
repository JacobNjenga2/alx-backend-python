import mysql.connector
import os

def stream_users_in_batches(batch_size):
    """Generator: fetch user_data in batches of size batch_size"""
    mysql_password = os.getenv("MYSQL_PASSWORD")
    if not mysql_password:
        raise Exception("Please set your MYSQL_PASSWORD environment variable.")

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=mysql_password,
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as count FROM user_data")
        total_rows = cursor.fetchone()['count']

        for offset in range(0, total_rows, batch_size):
            cursor.execute(
                f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
            )
            batch = cursor.fetchall()
            if batch:
                yield batch
    finally:
        cursor.close()
        conn.close()

def batch_processing(batch_size):
    """Process each batch: return users over age 25"""
    filtered_users = []
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            age = int(user['age'])  # convert age to int for safety
            if age > 25:
                print(user)
                filtered_users.append(user)
    return filtered_users