import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import os

# --- Config ---
st.set_page_config(page_title="Face Attendance Dashboard", layout="centered")

# --- Timestamp Setup ---
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
csv_path = f"Attendance/Attendance_{date}.csv"

# --- Title ---
st.title("📅 Real-time Attendance Dashboard")
st.caption(f"📍 Date: `{date}` | 🕒 Time: `{timestamp}`")

# --- Auto Refresh Counter (Every 2 seconds) ---
count = st_autorefresh(interval=2000, limit=1000, key="counter")

# --- FizzBuzz Section ---
st.subheader("🔁 FizzBuzz Counter")

if count == 0:
    st.info("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.success("FizzBuzz")
elif count % 3 == 0:
    st.warning("Fizz")
elif count % 5 == 0:
    st.warning("Buzz")
else:
    st.write(f"Count: `{count}`")

# --- Attendance Section ---
st.subheader("📋 Today's Attendance")

def load_attendance(file_path):
    if not os.path.exists(file_path):
        st.error(f"Attendance file not found for today: `{file_path}`")
        return None
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Failed to load attendance file: {e}")
        return None

df = load_attendance(csv_path)

if df is not None and not df.empty:
    st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
    st.success(f"Total Entries: {len(df)}")
else:
    st.warning("No attendance records found yet.")
