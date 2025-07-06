import mysql.connector
import os

def stream_users():
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv("MYSQL_PASSWORD"),   # ← Replace with your actual MySQL password
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    # Query all rows from user_data
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()
