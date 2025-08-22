import requests
from config import API_KEY, API_SECRET, BASE_URL

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET
}

try:
    response = requests.get(f"{BASE_URL}/v2/account", headers=HEADERS)
    if response.status_code == 200:
        print("✅ Connection successful.")
        print(response.json())
    else:
        print(f"❌ Failed to connect: {response.status_code}.")
except Exception as e:
    print(f"❌ Error: {e}")
