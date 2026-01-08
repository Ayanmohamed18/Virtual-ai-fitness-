import requests
import os
from dotenv import load_dotenv

# Try to load env and catch any errors
try:
    load_dotenv()
    print("Environment loaded.")
except Exception as e:
    print(f"Error loading .env: {e}")

api_key = os.getenv("RAPIDAPI_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"Key length: {len(api_key)}")
    print(f"Key start: {api_key[:5]}...")

url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/chest"
headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "exercisedb.p.rapidapi.com"
}

print(f"Testing URL: {url}")
try:
    response = requests.get(url, headers=headers, params={"limit": "1"})
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Received {len(data)} exercises.")
        if data:
            first_ex = data[0]
            print(f"Name: {first_ex.get('name')}")
            print(f"Gif URL: {first_ex.get('gifUrl')}")
            print("Keys found:")
            for k in first_ex.keys():
                print(f"- {k}")
    else:
        print("Request failed.")
        print(response.text)
except Exception as e:
    print(f"Exception error: {e}")
