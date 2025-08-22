from fetch_portfolio import get_portfolio
import streamlit as st
import json
import os
import subprocess
from datetime import datetime

st.set_page_config(page_title="🤖 AI Multi-Bot Dashboard", layout="wide")
st.title("🤖 AI Multi-Bot System Dashboard")
st.sidebar.title("⚙️ Controls")

# ---- SIDEBAR CONTROLS ----
if st.sidebar.button("📈 Simulate Profit"):
    st.success("📈 Simulating profitability... (placeholder)")
    st.info("📤 ROI export triggered... (placeholder)")

if st.sidebar.button("🩺 Run Health Sweep"):
    st.success("✅ Health check running via health_bot... (placeholder)")

if st.sidebar.button("📤 Push Logs to Google Sheets"):
    os.system("python export_to_sheets.py")
    st.success("✅ Logs pushed to Google Sheets!")

if st.sidebar.button("🔁 Refresh Memory Logs"):
    st.rerun()

if st.sidebar.button("📄 View Command Reference"):
    try:
        with open("docs/AI_Bot_Command_Reference.txt", "r") as f:
            st.code(f.read(), language="text")
    except FileNotFoundError:
        st.error("❌ Command Reference not found.")

# AI Logs Display
st.header("🧠 AI Memory Log")
if os.path.exists("ai_decisions.json"):
    with open("ai_decisions.json", "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
else:
    logs = []

if logs:
    for entry in reversed(logs[-10:]):
        if all(k in entry for k in ["timestamp", "strategy", "action", "reason"]):
            st.success(f"🕒 {entry['timestamp']} — **{entry['strategy']}**: {entry['action']} — _{entry['reason']}_")
        else:
            st.warning("⚠️ Skipping malformed log entry.")
else:
    st.info("No AI decisions logged yet.")

import subprocess

if st.sidebar.button("📊 Launch Portfolio Graph"):
    subprocess.Popen(["streamlit", "run", "portfolio_graph_gui.py"])
    st.sidebar.success("Graph launched in new tab.")

if st.sidebar.button("📤 Push Logs to Google Sheets"):
    os.system("python export_to_sheets.py")
    st.sidebar.success("✅ Logs pushed to Sheets")


# ---- BALANCE SHEET (Live) ----
from fetch_portfolio import get_portfolio

st.header("📊 Balance Sheet (Live Portfolio Snapshot)")
portfolio = get_portfolio()

if portfolio:
    st.write(f"📅 Last updated: {portfolio['timestamp']}")
    st.metric("💰 Equity", f"${portfolio['equity']}")
    st.metric("💵 Cash", f"${portfolio['cash']}")
    st.metric("📈 Buying Power", f"${portfolio['buying_power']}")
    st.metric("📊 Portfolio Value", f"${portfolio['portfolio_value']}")
    st.metric("📘 Long Market Value", f"${portfolio['long_market_value']}")
    st.metric("📕 Short Market Value", f"${portfolio['short_market_value']}")
    if portfolio["trading_blocked"]:
        st.error("🚫 Trading is currently blocked!")
    else:
        st.success("✅ Trading is active.")
else:
    st.warning("⚠️ Could not fetch portfolio.")


# Potential Profit Forecast Placeholder
st.header("💸 Potential Profit Projections")
st.write("This will simulate future profit based on structure, taxes, and wealth strategies:")
st.markdown("""
- 📁 LLC or S-Corp structure
- 🧾 Legal/tax deductions
- 📈 Compound gains
- 🛡️ Trust-based planning
""")

# Health Logs
if os.path.exists("logs/health_logs/health_log.json"):
    st.header("🩻 Latest Health Sweep")
    with open("logs/health_logs/health_log.json", "r") as f:
        try:
            health_log = json.load(f)
            for k, v in health_log.items():
                st.write(f"**{k}**: {v}")
        except json.JSONDecodeError:
            st.warning("⚠️ Could not parse health log.")
else:
    st.info("No health logs found.")
