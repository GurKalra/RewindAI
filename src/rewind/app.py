import streamlit as st
import pandas as pd
import time
import os
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="RewindAI | AMD Ryzen AI", page_icon="🛡️", layout="wide")

# --- Safety: Ensure data dir and status file exist ---
os.makedirs("data", exist_ok=True)
STATUS_FILE = "data/status.txt"

if not os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "w") as f:
        f.write("SAFE|System Initializing|0.00|0.0")

# --- UI Styling ---
st.title("🛡️ RewindAI: Real-Time Behavioral Shield 🛡️")
st.subheader("Hardware-Accelerated Ransomware Defense (AMD Slingshot MVP)")

# Initialize session state for the chart history
if 'score_history' not in st.session_state:
    st.session_state.score_history = [0.0] * 50

# --- Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Security Pulse")
    status_box = st.empty()
    metric_box = st.empty()
    file_box = st.empty()

with col2:
    st.header("AI Threat Confidence (Live)")
    chart_placeholder = st.empty()

# --- Live Update Loop ---
while True:
    try:
        with open(STATUS_FILE, "r") as f:
            line = f.read().strip()
            if not line: continue
            data = line.split("|")
            
        status, filename, score, timestamp = data[0], data[1], float(data[2]), float(data[3])
        
        # Update History
        st.session_state.score_history.append(score)
        if len(st.session_state.score_history) > 50:
            st.session_state.score_history.pop(0)

        # SAFE STATE
        if status == "SAFE":
            status_box.success("✅ SYSTEM SECURE")
            metric_box.metric("Threat Probability", f"{score*100:.1f}%", delta="Normal", delta_color="normal")
            file_box.info(f"Last File Scanned: {filename}")
        
        # ATTACK STATE
        else:
            status_box.error("🚨 RANSOMWARE ACTIVITY DETECTED")
            metric_box.metric("Threat Probability", f"{score*100:.1f}%", delta="CRITICAL", delta_color="inverse")
            file_box.warning(f"Targeted File: {filename}")
            st.toast(f"RewindAI: Restored {filename} instantly!", icon="🛡️")

        # Update Chart
        chart_placeholder.area_chart(st.session_state.score_history)

    except Exception as e:
        st.error(f"Waiting for Monitor: {e}")

    time.sleep(0.5) # Refresh rate (AMD Ryzen AI can handle much faster, but 0.5 is good for UI)