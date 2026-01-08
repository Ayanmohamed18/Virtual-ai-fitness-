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
if not api_key:
    # Use the key provided by user if env is missing
    api_key = "23a13b114dmsh97d7eb0f501d612p158e89jsn3aa4ce88aa5f"

print(f"API Key: {api_key[:5]}...")

url = "https://musclewiki-api.p.rapidapi.com/exercises"
headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "musclewiki-api.p.rapidapi.com"
}

# Test searching for 'curl'
print(f"Testing URL: {url}")
try:
    response = requests.get(url, headers=headers, params={"name": "Barbell Curl", "limit": "1"})
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Received {len(data)} exercises.")
        if 'results' in data and data['results']:
            ex = data['results'][0]
            print(f"First Result: {ex}")
            
            # Try fetching details by ID
            ex_id = ex['id']
            detail_url = f"https://musclewiki-api.p.rapidapi.com/exercises/{ex_id}"
            print(f"Testing Detail URL: {detail_url}")
            resp2 = requests.get(detail_url, headers=headers)
            if resp2.status_code == 200:
                details = resp2.json()
                import json
                with open("mw_response.json", "w") as f:
                    json.dump(details, f, indent=4)
                print("Dumped full details to mw_response.json")
            else:
                print(f"Detail Request Failed: {resp2.status_code}")
        else:
            print("No results found.")
    else:
        print("Request failed.")
        print(response.text)
except Exception as e:
    print(f"Exception error: {e}")
