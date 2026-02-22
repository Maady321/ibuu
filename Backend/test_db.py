import pg8000
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection(user, password, host, port, database, driver_name):
    print(f"\n--- Testing {driver_name} ---")
    print(f"User: {user}, Password: {'*' * len(password)}, DB: {database}")
    try:
        if driver_name == "pg8000":
            conn = pg8000.connect(user=user, password=password, host=host, port=port, database=database)
        else:
            conn = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        print(f"SUCCESS with {driver_name}!")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILURE with {driver_name}: {e}")
        return False

# Common params
host = "localhost"
port = 5432
database = "ibbu"
user = "postgres"

# Test both passwords
passwords = ["Maady@321", "Maady_321"]

for pwd in passwords:
    print(f"\n>>> TRYING PASSWORD: {pwd}")
    test_connection(user, pwd, host, port, database, "psycopg2")
    test_connection(user, pwd, host, port, database, "pg8000")
