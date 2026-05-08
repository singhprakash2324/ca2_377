import streamlit as st
import psutil
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


# Page config
st.set_page_config(
    page_title="Real-Time System Monitor",
    page_icon="📊",
    layout="wide"
)

# Auto refresh every 2 seconds
st_autorefresh(interval=2000, key="system_monitor")



st.title("🚀 Real-Time System Monitoring Dashboard")

# Session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Time", "CPU", "Memory"]
    )

# Collect metrics
cpu_usage = psutil.cpu_percent()
memory_info = psutil.virtual_memory()
disk_info = psutil.disk_usage('/')

current_time = datetime.now().strftime("%H:%M:%S")

# Store data
new_row = pd.DataFrame({
    "Time": [current_time],
    "CPU": [cpu_usage],
    "Memory": [memory_info.percent]
})

st.session_state.data = pd.concat(
    [st.session_state.data, new_row],
    ignore_index=True
).tail(20)

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("CPU Usage", f"{cpu_usage}%")
col2.metric(
    "Memory Usage",
    f"{memory_info.percent}%",
    f"{memory_info.available // (1024**2)} MB Available"
)
col3.metric("Disk Usage", f"{disk_info.percent}%")

# Charts
st.subheader("📈 System Performance")

chart_data = st.session_state.data.set_index("Time")
st.line_chart(chart_data)

# Top processes
st.subheader("⚙️ Top Processes")

processes = []

for proc in psutil.process_iter(
    ['pid', 'name', 'cpu_percent', 'memory_percent']
):
    processes.append(proc.info)

df_proc = pd.DataFrame(processes)

df_proc = df_proc.sort_values(
    by='cpu_percent',
    ascending=False
).head(5)

st.dataframe(df_proc)