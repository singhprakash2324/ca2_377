import streamlit as st
import psutil
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import humanize # Import humanize for better size formatting


# Page config
st.set_page_config(
    page_title="Real-Time System Monitor",
    page_icon="📊",
    layout="wide"
)

# Auto refresh every 2 seconds
st_autorefresh(interval=2000, key="system_monitor")



st.title("🚀 Real-Time System Monitoring Dashboard")

# Create tabs
tab1, tab2 = st.tabs(["Overview", "Processes"])

with tab1:
    st.subheader("📊 System Overview")
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

    with col1:
        st.metric("CPU Usage", f"{cpu_usage}%")
    with col2:
        st.metric(
            "Memory Usage",
            f"{memory_info.percent}%",
            f"{humanize.naturalsize(memory_info.used)} used / {humanize.naturalsize(memory_info.total)} total"
        )
    with col3:
        st.metric(
            "Disk Usage",
            f"{disk_info.percent}%",
            f"{humanize.naturalsize(disk_info.used)} used / {humanize.naturalsize(disk_info.total)} total"
        )

    # Charts
    st.subheader("📈 System Performance")

    chart_data = st.session_state.data.set_index("Time")
    st.line_chart(chart_data)

with tab2:
    st.subheader("⚙️ Top Processes")

    processes = []

    for proc in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent', 'username', 'status', 'num_threads', 'memory_info']
    ):
        try:
            pinfo = proc.info
            if pinfo['memory_info'] is not None:
                pinfo['rss_mb'] = pinfo['memory_info'].rss / (1024 * 1024)
                pinfo['vms_mb'] = pinfo['memory_info'].vms / (1024 * 1024)
            else:
                pinfo['rss_mb'] = 0
                pinfo['vms_mb'] = 0
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    df_proc = pd.DataFrame(processes)

    df_proc = df_proc.sort_values(
        by='cpu_percent',
        ascending=False
    ).head(10) # Display top 10 processes

    # Select and rename columns for better display
    df_proc = df_proc[['name', 'pid', 'username', 'status', 'cpu_percent', 'memory_percent', 'rss_mb', 'vms_mb', 'num_threads']]
    df_proc.columns = ['Process Name', 'PID', 'User', 'Status', 'CPU %', 'Memory %', 'RSS (MB)', 'VMS (MB)', 'Threads']

    st.dataframe(df_proc)