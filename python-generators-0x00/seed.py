#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os


# 🧠 Centralize credentials for easy maintenance
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),  # Ideally, use os.getenv("MYSQL_PASSWORD")
    "database": "ALX_prodev"
}


def connect_db():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"]
        )
        return connection
    except Error as err:
        print(f"❌ Connection error (DB setup): {err}")
        return None


def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("✅ Database ALX_prodev created successfully")
    except Error as err:
        print(f"❌ Error creating database: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"]
        )
        return connection
    except Error as err:
        print(f"❌ Connection error (ALX_prodev): {err}")
        return None


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age DECIMAL NOT NULL
            );
        """)
        print("✅ Table user_data created successfully")
    except Error as err:
        print(f"❌ Error creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inserted = 0
            for row in reader:
                cursor.execute("SELECT * FROM user_data WHERE email=%s", (row['email'],))
                if not cursor.fetchone():
                    user_id = str(uuid.uuid4())
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, row['name'], row['email'], row['age']))
                    inserted += 1
        connection.commit()
        print(f"✅ Data inserted successfully: {inserted} new entries")
    except FileNotFoundError:
        print(f"❌ CSV file '{csv_file}' not found")
    except Error as err:
        print(f"❌ Error inserting data: {err}")
    finally:
        cursor.close()