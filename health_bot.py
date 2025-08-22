import os
import ast
import json
import csv
from datetime import datetime
from communications_bot import send_health_report

HEALTH_LOG = "bot_health_log.csv"
AI_LOG = "ai_decisions.json"

# Core folders and files to check
FOLDERS = ["."]  # Current directory only for now
EXTENSIONS = [".py"]


def scan_file_for_issues(filepath):
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
            ast.parse(code)  # Syntax check
    except SyntaxError as e:
        issues.append(f"Syntax error: {e}")
    except Exception as e:
        issues.append(f"General error: {e}")
    return issues


def run_health_sweep():
    # (your sweep logic above)
    
    print("✅ Health sweep completed.")
    os.system("python export_to_sheets.py")
    print("✅ Health results exported to Google Sheets.")


    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_report = []

    for root, _, files in os.walk("."):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                path = os.path.join(root, file)
                issues = scan_file_for_issues(path)
                if issues:
                    full_report.append({
                        "timestamp": timestamp,
                        "file": path,
                        "issues": issues
                    })

    write_health_log(full_report)
    notify_ai_bot(full_report)
    send_health_report(bot_name="Health Bot", issue=full_report)
    print("✅ Health sweep completed.")


def write_health_log(report):
    if not report:
        return

    with open(HEALTH_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        for entry in report:
            writer.writerow([entry["timestamp"], entry["file"], " | ".join(entry["issues"])])


def notify_ai_bot(report):
    if not report:
        return

    try:
        with open(AI_LOG, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    for entry in report:
        logs.append({
            "timestamp": entry["timestamp"],
            "strategy": "Health Monitor",
            "action": f"Detected issues in {os.path.basename(entry['file'])}",
            "reason": entry["issues"][:1][0]  # Only the first issue
        })

    with open(AI_LOG, "w") as f:
        json.dump(logs, f, indent=4)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-sweep", action="store_true", help="Run full bot health scan")
    args = parser.parse_args()

    if args.full_sweep:
        run_health_sweep()
    else:
        print("Use --full-sweep to perform scan.")
