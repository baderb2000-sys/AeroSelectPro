import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AeroSelect Pro",
    page_icon="❄️",
    layout="wide"
)

# =========================
# STYLE
# =========================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #4FC3F7;
}

[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #333;
    padding: 15px;
    border-radius: 10px;
}

.stButton>button {
    background-color: #0288D1;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("❄️ AeroSelect Pro")
st.subheader("Professional HVAC Diffuser Selection Tool")

st.markdown("---")

# =========================
# SIDEBAR
# =========================

st.sidebar.header("Design Inputs")

room_length = st.sidebar.number_input(
    "Room Length (ft)",
    min_value=1.0,
    value=20.0
)

room_width = st.sidebar.number_input(
    "Room Width (ft)",
    min_value=1.0,
    value=15.0
)

room_height = st.sidebar.number_input(
    "Room Height (ft)",
    min_value=1.0,
    value=10.0
)

airflow = st.sidebar.number_input(
    "Airflow (CFM)",
    min_value=1.0,
    value=800.0
)

throw_distance = st.sidebar.number_input(
    "Throw Distance (ft)",
    min_value=1.0,
    value=12.0
)

# =========================
# CALCULATIONS
# =========================

room_volume = room_length * room_width * room_height

ach = (airflow * 60) / room_volume

velocity = airflow / (room_width * room_height)

# =========================
# KPIs
# =========================

st.subheader("📊 Engineering Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Room Volume", f"{room_volume:.1f} ft³")

with col2:
    st.metric("Air Changes Per Hour", f"{ach:.1f}")

with col3:
    st.metric("Air Velocity", f"{velocity:.1f} FPM")

# =========================
# RECOMMENDATIONS
# =========================

st.subheader("🤖 Smart HVAC Recommendation")

if velocity < 300:
    st.success("Excellent airflow distribution.")

elif velocity < 500:
    st.warning("Moderate airflow detected.")

else:
    st.error("High airflow velocity detected.")

# =========================
# CHART
# =========================

st.subheader("📈 HVAC Performance")

chart_data = pd.DataFrame({
    "Parameter": ["ACH", "Velocity", "Airflow"],
    "Value": [ach, velocity, airflow]
})

fig = px.bar(
    chart_data,
    x="Parameter",
    y="Value",
    title="HVAC Analysis"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABLE
# =========================

st.subheader("📋 Design Summary")

summary = pd.DataFrame({
    "Parameter": [
        "Room Length",
        "Room Width",
        "Room Height",
        "Room Volume",
        "Airflow",
        "Velocity",
        "ACH"
    ],
    "Value": [
        room_length,
        room_width,
        room_height,
        room_volume,
        airflow,
        velocity,
        ach
    ]
})

st.dataframe(summary, use_container_width=True)

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption("AeroSelect Pro • HVAC Engineering Platform")