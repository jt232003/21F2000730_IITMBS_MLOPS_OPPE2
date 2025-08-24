# send_requests.py
import requests
import json
import time

API_ENDPOINT = "http://34.57.163.156/predict"
HEADERS = {"Content-Type": "application/json"}

with open('random_samples.jsonl', 'r') as f:
    for i, line in enumerate(f):
        # Convert the line (which is a string) into a Python dictionary
        data = json.loads(line)

        try:
            # Send the POST request
            response = requests.post(API_ENDPOINT, headers=HEADERS, json=data)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            print(f"Sample {i+1}: Sent data, received prediction: {response.json()}")

        except requests.exceptions.RequestException as e:
            print(f"Sample {i+1}: Request failed: {e}")

        # Pause for a moment to not overwhelm the API
        time.sleep(0.5)

print("\nFinished sending all requests.")