import requests
import json

url = "http://127.0.0.1:8000/api/auth/register"
payload = {
    "name": "Test User",
    "email": "string@gmail.com",
    "password": "string@321",
    "phone": "7777777777",
    "address": "Street"
}
headers = {'Content-Type': 'application/json'}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
