# portfolio_graph_gui.py

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "logs/portfolio_history/portfolio_snapshots.json"

st.set_page_config(page_title="📈 Portfolio Graph", layout="wide")
st.title("📈 Live Portfolio Graph")

# Toggle buttons
show_equity = st.checkbox("Show Equity", value=True)
show_cash = st.checkbox("Show Cash", value=True)
show_total = st.checkbox("Show Total Portfolio Value", value=True)

if not os.path.exists(LOG_FILE):
    st.error("❌ portfolio_snapshots.json not found.")
    st.stop()

with open(LOG_FILE, "r") as f:
    snapshots = json.load(f)

if not snapshots:
    st.warning("⚠️ No snapshot data available.")
    st.stop()

# Build DataFrame
df = pd.DataFrame(snapshots)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Convert types
df['equity'] = pd.to_numeric(df['equity'], errors='coerce')
df['cash'] = pd.to_numeric(df['cash'], errors='coerce')
df['total_value'] = df['equity'] + df['cash']

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

if show_equity:
    ax.plot(df['timestamp'], df['equity'], label='Equity', marker='o')
if show_cash:
    ax.plot(df['timestamp'], df['cash'], label='Cash', linestyle='--', marker='x')
if show_total:
    ax.plot(df['timestamp'], df['total_value'], label='Total Value', linewidth=2, color='green')

ax.set_xlabel("Timestamp")
ax.set_ylabel("Value ($)")
ax.set_title("Portfolio Snapshot Over Time")
ax.legend()
ax.grid(True)

st.pyplot(fig)
