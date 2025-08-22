# fixer_tool.py

import json
import os

def fix_json_logs():
    """
    Cleans ai_decisions.json by removing empty or malformed entries.
    """
    file_path = "ai_decisions.json"
    if not os.path.exists(file_path):
        print("🧼 No ai_decisions.json found to clean.")
        return

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ JSON decode error — file reset.")
            data = []

    # Filter out malformed entries
    cleaned = [
        entry for entry in data
        if isinstance(entry, dict) and all(k in entry for k in ["timestamp", "strategy", "action", "reason"])
    ]

    with open(file_path, "w") as f:
        json.dump(cleaned, f, indent=4)

    print(f"🧹 Cleaned {len(data) - len(cleaned)} bad entries from ai_decisions.json.")
