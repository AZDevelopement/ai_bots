# log_portfolio_snapshot.py

import os
import json
from datetime import datetime
import requests
from config import API_KEY, API_SECRET, BASE_URL

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET
}

def fetch_account():
    try:
        response = requests.get(f"{BASE_URL}/v2/account", headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch account data: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def log_snapshot():
    account = fetch_account()
    if account:
        snapshot = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "equity": f"${account.get('equity', '0')}",
            "cash": f"${account.get('cash', '0')}",
            "buying_power": f"${account.get('buying_power', '0')}",
            "portfolio_value": f"${account.get('portfolio_value', '0')}"
        }

        os.makedirs("logs/portfolio_history", exist_ok=True)
        filepath = "logs/portfolio_history/portfolio_snapshots.json"

        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        data.append(snapshot)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Portfolio snapshot logged.")
    else:
        print("⚠️ No snapshot logged due to account fetch failure.")

if __name__ == "__main__":
    log_snapshot()

if __name__ == "__main__":
    log_portfolio_to_sheets()
    print("✅ Portfolio snapshots pushed to Google Sheets.")

