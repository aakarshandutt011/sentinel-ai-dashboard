import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sentinal AI - Threat Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (The "Cyberpunk" Look) ---
st.markdown("""
    <style>
        /* Main Background */
        .stApp {
            background-color: #0e1117;
        }
        
        /* Metric Cards (Glassmorphism) */
        div[data-testid="metric-container"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            color: white;
            transition: transform 0.2s;
        }
        div[data-testid="metric-container"]:hover {
            transform: scale(1.02);
            border: 1px solid #00ffea;
            box-shadow: 0 0 15px rgba(0, 255, 234, 0.3);
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #050510;
        }
        
        /* Custom Headers */
        h1, h2, h3 {
            color: #00ffea !important;
            font-family: 'Courier New', monospace;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTION FOR ANIMATION ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a "Security Scan" animation
lottie_security = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

# --- 4. DATA LOADING ---
try:
    df = pd.read_csv('server_logs.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
except:
    st.error("⚠️ Data not found! Run generate_data.py first.")
    st.stop()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9203/9203764.png", width=100)
    st.title("SENTINEL AI")
    st.markdown("---")
    st.write("System Status: **🟢 ONLINE**")
    st.write(f"Monitoring Nodes: **{df['Source_IP'].nunique()}**")
    st.markdown("---")
    upload = st.file_uploader("📂 Ingest New Logs", type='csv')
    if upload:
        df = pd.read_csv(upload)

# --- 6. MAIN LAYOUT ---

# Top Banner
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🛡️ Security Operations Center")
    st.markdown("Artificial Intelligence Log Analysis & Threat Detection")
with col2:
    if lottie_security:
        st_lottie(lottie_security, height=100, key="security_anim")

st.markdown("---")

# KPI ROW (The "Heads Up Display")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_reqs = len(df)
failed_reqs = len(df[df['Status_Code'] != 200])
attack_reqs = len(df[df['Status_Code'] == 401]) # Brute force
sql_reqs = len(df[df['Status_Code'] == 500])    # SQLi often causes 500s

kpi1.metric("Total Traffic", f"{total_reqs}", "Requests")
kpi2.metric("Failed Requests", f"{failed_reqs}", "-2% vs avg")
kpi3.metric("Brute Force Alerts", f"{attack_reqs}", "High Risk", delta_color="inverse")
kpi4.metric("SQLi Attempts", f"{sql_reqs}", "Critical", delta_color="inverse")

st.markdown("### 📉 Real-Time Threat Traffic")

# --- 7. PLOTLY CHARTS (The "Neon" Look) ---
# Create a time-series chart
hourly_counts = df.set_index('Timestamp').resample('H').size().reset_index(name='Count')

# Define colors based on threshold (Red if traffic is unusually high)
hourly_counts['Risk'] = ['Critical' if x > 80 else 'Normal' for x in hourly_counts['Count']]
color_map = {'Normal': '#00ffea', 'Critical': '#ff0055'}

fig = px.bar(
    hourly_counts, 
    x='Timestamp', 
    y='Count',
    color='Risk',
    color_discrete_map=color_map,
    template='plotly_dark',
    title="Traffic Volume vs Anomaly Detection"
)

# Customizing the chart to look Cyberpunk
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)
st.plotly_chart(fig, use_container_width=True)

# --- 8. DETAILED ANALYSIS (Split View) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("🚨 Top Attacking IPs")
    # Count requests by IP
    ip_counts = df['Source_IP'].value_counts().reset_index()
    ip_counts.columns = ['IP Address', 'Request Count']
    
    # Donut Chart
    fig2 = px.pie(
        ip_counts, 
        values='Request Count', 
        names='IP Address', 
        hole=0.6,
        template='plotly_dark',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    st.subheader("🔍 Endpoint Vulnerability Map")
    # Heatmap of Endpoints vs Status Codes
    # Filter for interesting data only
    vuln_data = df[df['Status_Code'] != 200]
    st.dataframe(
        vuln_data[['Timestamp', 'Source_IP', 'Endpoint', 'Status_Code']].sort_values(by="Timestamp", ascending=False),
        height=300,
        use_container_width=True
    )

# --- 9. AI CHAT INTERFACE (Placeholder for next step) ---
st.markdown("---")
st.subheader("🤖 AI Security Analyst")
user_input = st.text_input("Ask the AI about your logs (e.g., 'Show me all attacks from IP 192.168.1.666')")
if user_input:
    st.info(f"AI Analysis Module Initializing... processing query: '{user_input}'")
    # This is where we will hook up OpenAI in the next step!
# 1. Page Config (Tab Title)
st.set_page_config(page_title="AI Security Analyst", layout="wide")

# 2. Title & Intro
st.title("🤖 AI-Powered Log Analyst")
st.markdown("Upload your server logs and ask questions about potential threats.")

# 3. Sidebar for File Upload
with st.sidebar:
    st.header("1. Upload Logs")
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    
    # If no file uploaded, load the fake one we generated
    if uploaded_file is None:
        st.info("Using generated demo data (server_logs.csv)")
        try:
            df = pd.read_csv('server_logs.csv')
        except:
            st.error("Run generate_data.py first!")
            st.stop()
    else:
        df = pd.read_csv(uploaded_file)

# 4. Show Raw Data (The "Ingest" Visual)
st.subheader("📊 Live Log Ingestion")
# Show the first 5 rows
st.dataframe(df.head())

# 5. Basic Statistics (Hardcoded for now)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Logs", len(df))
with col2:
    st.metric("Unique IPs", df['Source_IP'].nunique())
with col3:
    error_count = len(df[df['Status_Code'] != 200])
    st.metric("Error/Attack Rates", error_count)

# 6. A Simple Chart (Hardcoded)
st.subheader("Traffic Over Time")
# Convert timestamp string to datetime object for plotting
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
# Count logs per hour
hourly_counts = df.set_index('Timestamp').resample('H').size()
st.line_chart(hourly_counts)
