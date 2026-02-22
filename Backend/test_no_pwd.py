import psycopg2
import os

print("--- Testing No Password ---")
try:
    conn = psycopg2.connect(user="postgres", host="127.0.0.1", port=5432, database="postgres")
    print("SUCCESS with 127.0.0.1 and no password!")
    conn.close()
except Exception as e:
    print(f"FAILURE with 127.0.0.1 and no password: {e}")

try:
    conn = psycopg2.connect(user="postgres", host="localhost", port=5432, database="postgres")
    print("SUCCESS with localhost and no password!")
    conn.close()
except Exception as e:
    print(f"FAILURE with localhost and no password: {e}")
