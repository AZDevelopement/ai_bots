# export_to_sheets.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import os

# ---- CONFIGURATION ----
GOOGLE_SHEET_NAME = "TradingBotLogs"
AI_LOG_SHEET = "AI Decisions"
ROI_SHEET = "ROI Logs"
HEALTH_SHEET = "Health Logs"
CREDENTIALS_FILE = "credentials.json"

# ---- GOOGLE SHEETS AUTH ----
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# ---- UTILITY: Write to sheet ----
def export_json_to_sheet(json_file, sheet_name, headers):
    try:
        sheet = client.open(GOOGLE_SHEET_NAME).worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet = client.open(GOOGLE_SHEET_NAME).add_worksheet(title=sheet_name, rows="100", cols="20")
        sheet.append_row(headers)

    if not os.path.exists(json_file):
        print(f"⚠️ File not found: {json_file}")
        return

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Could not read {json_file}")
            return

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        print(f"⚠️ Invalid format in {json_file}")
        return

    for row in data:
        if all(h in row for h in headers):
            sheet.append_row([row[h] for h in headers])

# ---- EXPORT AI DECISIONS ----
export_json_to_sheet("ai_decisions.json", AI_LOG_SHEET, ["timestamp", "strategy", "action", "reason"])

# ---- EXPORT ROI LOGS ----
export_json_to_sheet("logs/roi_log.json", ROI_SHEET, ["timestamp", "ROI", "notes"])

# ---- EXPORT HEALTH LOGS ----
export_json_to_sheet("logs/health_logs/health_log.json", HEALTH_SHEET, ["timestamp", "status", "issues"])

print("✅ Export completed.")
