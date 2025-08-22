import json
import os
from datetime import datetime

class ProfitabilityBot:
    def __init__(self, log_file="profitability_log.json"):
        self.log_file = log_file
        self.profit_log = []
        self.load_log()

    def load_log(self):
        try:
            with open(self.log_file, "r") as f:
                self.profit_log = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.profit_log = []

    def save_log(self):
        with open(self.log_file, "w") as f:
            json.dump(self.profit_log, f, indent=4)

    def record_trade(self, symbol, amount_invested, amount_returned, strategy, notes=""):
        pnl = amount_returned - amount_invested
        roi = (pnl / amount_invested) * 100 if amount_invested != 0 else 0

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "invested": amount_invested,
            "returned": amount_returned,
            "pnl": pnl,
            "roi_percent": round(roi, 2),
            "strategy": strategy,
            "notes": notes
        }

        self.profit_log.append(entry)
        self.save_log()
        print(f"✅ Recorded trade for {symbol}: PnL=${pnl:.2f} | ROI={roi:.2f}%")

    def get_total_pnl(self):
        return sum(entry["pnl"] for entry in self.profit_log)

    def get_roi_by_strategy(self):
        strategies = {}
        for entry in self.profit_log:
            strat = entry["strategy"]
            if strat not in strategies:
                strategies[strat] = {"pnl": 0, "count": 0}
            strategies[strat]["pnl"] += entry["pnl"]
            strategies[strat]["count"] += 1

        for strat, stats in strategies.items():
            stats["avg_pnl"] = round(stats["pnl"] / stats["count"], 2)

        return strategies

# Test mode if run directly
if __name__ == "__main__":
    pb = ProfitabilityBot()
    pb.record_trade("AAPL", 1000, 1100, "SMA-RSI Combo", "Good entry timing")
    print(f"Total PnL: ${pb.get_total_pnl():.2f}")
    print("ROI by Strategy:", pb.get_roi_by_strategy())

# After bot logic finishes
import os

try:
    os.system("python log_portfolio_snapshot.py")
    print("📸 Portfolio snapshot saved.")

    os.system("python export_to_sheets.py")
    print("✅ Logs + snapshot pushed to Google Sheets.")
except Exception as e:
    print(f"❌ Error in auto-export: {e}")



