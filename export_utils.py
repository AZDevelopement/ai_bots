# export_utils.py
import os

def run_export_to_sheets():
    try:
        result = os.system("python export_to_sheets.py")
        if result == 0:
            print("✅ Export to Google Sheets completed successfully.")
        else:
            print("❌ Export script ran but failed. Check export_to_sheets.py for issues.")
    except Exception as e:
        print(f"❌ Failed to run export_to_sheets.py: {e}")

# Optional manual test (you can comment this out if importing elsewhere)
if __name__ == "__main__":
    run_export_to_sheets()
