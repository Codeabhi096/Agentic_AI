import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Webhook URL (Default to test webhook or environment variable)
url = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://firstproject7208.app.n8n.cloud/webhook-test/783ce764-7ce6-4647-8de0-7c38ad0d4d21"
)

user_message = "can you tell me about super intelligence in 3 to 4 lines?"
request_message = {"message": user_message}

print(f"📡 Sending request to: {url}")
print(f"💬 Message: {user_message}\n")

try:
    response = requests.post(url, json=request_message, timeout=60)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    if isinstance(data, list) and len(data) > 0 and "output" in data[0]:
        print("\n🤖 Assistant Output:\n" + data[0]["output"])
    elif isinstance(data, dict) and "output" in data:
        print("\n🤖 Assistant Output:\n" + data["output"])
    else:
        print("\n🤖 Raw Response:\n", data)
except Exception as e:
    print(f"❌ Error communicating with webhook: {e}")
