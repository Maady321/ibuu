import psycopg2
import os

pwd = "Maady@321"
print(f"--- Testing 127.0.0.1 with password {pwd} ---")
try:
    conn = psycopg2.connect(user="postgres", password=pwd, host="127.0.0.1", port=5432, database="postgres")
    print("SUCCESS with 127.0.0.1 and password!")
    conn.close()
except Exception as e:
    print(f"FAILURE: {e}")
