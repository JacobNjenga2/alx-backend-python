#!/usr/bin/python3

import seed
import mysql.connector
from mysql.connector import Error

def main():
    try:
        # Connect and create the database
        connection = seed.connect_db()
        if connection:
            seed.create_database(connection)
            connection.close()
            print("✅ Database created")

        # Connect to the newly created database
        connection = seed.connect_to_prodev()
        if not connection:
            print("❌ Failed to connect to ALX_prodev")
            return

        print("✅ Connection to ALX_prodev successful")

        # Create table and insert data
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')

        # Query schema to confirm
        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("✅ Database ALX_prodev is present")

        # Fetch sample data
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print("📊 Sample Data from user_data table:")
        for row in rows:
            print(row)

        cursor.close()
        connection.close()

    except Error as err:
        print(f"❌ MySQL Error: {err}")
    except Exception as e:
        print(f"❌ General Error: {e}")

if __name__ == "__main__":
    main()
