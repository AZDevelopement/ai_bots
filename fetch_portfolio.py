# fetch_portfolio.py

import requests
from datetime import datetime
from config import API_KEY, API_SECRET, BASE_URL

def get_portfolio():
    url = f"{BASE_URL}/v2/account"
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": API_SECRET
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # ✅ Add timestamp to the portfolio snapshot
            data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return data
        else:
            print(f"❌ Failed to fetch portfolio: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching portfolio: {e}")
        return None
