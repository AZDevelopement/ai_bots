# ai_bot.py

import json
import os
from datetime import datetime
from profitability_bot import ProfitabilityBot
from math_bot import perform_stat_analysis  # Now exists
from communications_bot import send_health_report  # If applicable
from fixer_tool import fix_json_logs  # Optional fixer, safe to import

DECISION_LOG = "ai_decisions.json"

def make_ai_decision():
    """
    Simulate AI decision-making process.
    """
    decision = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strategy": "ProfitMax Strategy",
        "action": "Buy AAPL",
        "reason": "Strong RSI + Positive sentiment"
    }
    print("📌 Logging AI decision...")
    log_ai_decision(decision)
    return decision

def log_ai_decision(decision):
    if not os.path.exists(DECISION_LOG):
        with open(DECISION_LOG, "w") as f:
            json.dump([decision], f, indent=4)
        return

    with open(DECISION_LOG, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append(decision)

    with open(DECISION_LOG, "w") as f:
        json.dump(data, f, indent=4)

def simulate_trade(decision):
    """
    Pass the decision into ProfitabilityBot and log results.
    """
    pb = ProfitabilityBot()
    amount_invested = 1000
    amount_returned = 1100  # Simulate 10% gain
    pb.record_trade(
        symbol="AAPL",
        amount_invested=amount_invested,
        amount_returned=amount_returned,
        strategy=decision["strategy"],
        notes="Simulated trade"
    )

def run_stat_analysis():
    """
    Use math_bot (placeholder) for analysis.
    """
    print("📊 Running statistical analysis...")
    result = perform_stat_analysis()
    print("🧮 Result:", result)

def run_export():
    """
    Export all logs to Google Sheets.
    """
    print("📤 Exporting logs to Google Sheets...")
    try:
        os.system("python export_to_sheets.py")
        print("✅ Export to Google Sheets completed.")
    except Exception as e:
        print(f"❌ Export failed: {e}")

if __name__ == "__main__":
    print("🚀 AI Bot starting...")
    fix_json_logs()  # Optional fixer pass
    decision = make_ai_decision()
    simulate_trade(decision)
    run_stat_analysis()
    run_export()
    print("✅ AI Bot completed.")

# After bot logic finishes
import os

try:
    os.system("python log_portfolio_snapshot.py")
    print("📸 Portfolio snapshot saved.")

    os.system("python export_to_sheets.py")
    print("✅ Logs + snapshot pushed to Google Sheets.")
except Exception as e:
    print(f"❌ Error in auto-export: {e}")

