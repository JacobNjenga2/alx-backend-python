import mysql.connector
import os

def stream_user_ages():
    """Generator: yields user ages one by one from user_data table"""
    mysql_password = os.getenv("MYSQL_PASSWORD")
    if not mysql_password:
        raise Exception("Please set your MYSQL_PASSWORD environment variable.")

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=mysql_password,
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:
            yield int(age)
    finally:
        cursor.close()
        conn.close()

def average_user_age():
    """Calculates and prints the average age of all users using a generator"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    average_user_age()
