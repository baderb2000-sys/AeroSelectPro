import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import math

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AeroSelect Pro",
    page_icon="❄️",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}

.metric-box {
    background: #1B1F2A;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(0,255,255,0.2);
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("❄️ AeroSelect Pro")
st.subheader("Professional HVAC Diffuser Selection Tool")

st.markdown("""
This application helps HVAC engineers:

✅ Calculate airflow requirements  
✅ Estimate air velocity  
✅ Select suitable diffuser types  
✅ Compare diffuser performance  
✅ Estimate noise level and cooling load  
✅ Generate professional PDF reports  
""")

st.markdown("---")

# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.header("📌 Design Inputs")

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

people = st.sidebar.number_input(
    "Number of People",
    min_value=1,
    value=5
)

temperature = st.sidebar.slider(
    "Room Temperature (°C)",
    16,
    35,
    24
)

diffuser = st.sidebar.selectbox(
    "Select Diffuser Type",
    [
        "Ceiling Diffuser",
        "Slot Diffuser",
        "Linear Diffuser",
        "Swirl Diffuser",
        "Jet Diffuser"
    ]
)

# =========================
# VALIDATION
# =========================

if room_length <= 0 or room_width <= 0 or room_height <= 0:
    st.error("❌ Room dimensions must be greater than zero")
    st.stop()

# =========================
# CALCULATIONS
# =========================

room_area = room_length * room_width
room_volume = room_area * room_height

cfm = room_area * 1.2 + (people * 20)

velocity = cfm / 100

noise = velocity * 1.5

cooling_load = room_area * 25

power_kw = cooling_load / 3412

# =========================
# AUTO RECOMMENDATION
# =========================

if cfm < 300:
    recommended = "Ceiling Diffuser"

elif cfm < 500:
    recommended = "Linear Diffuser"

elif cfm < 800:
    recommended = "Swirl Diffuser"

else:
    recommended = "Jet Diffuser"

# =========================
# KPI CARDS
# =========================

st.header("📊 HVAC Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Airflow (CFM)", f"{cfm:.1f}")

with col2:
    st.metric("Velocity (FPM)", f"{velocity:.1f}")

with col3:
    st.metric("Noise (NC)", f"{noise:.1f}")

with col4:
    st.metric("Cooling Load", f"{cooling_load:.1f} BTU/h")

# =========================
# RESULTS
# =========================

st.markdown("---")

st.header("📌 Results Summary")

st.write(f"### Recommended Diffuser: ✅ {recommended}")

st.info(f"""
The system selected **{recommended}** because the required airflow is **{cfm:.1f} CFM**.

- Lower airflow → Ceiling Diffuser
- Medium airflow → Linear or Swirl Diffuser
- High airflow → Jet Diffuser
""")

# =========================
# COMPARISON TABLE
# =========================

st.header("📋 Diffuser Comparison")

comparison_df = pd.DataFrame({
    "Diffuser": [
        "Ceiling",
        "Linear",
        "Swirl",
        "Jet"
    ],
    "Airflow Range": [
        "100-300",
        "300-500",
        "500-800",
        "800+"
    ],
    "Noise Level": [
        "Low",
        "Medium",
        "Medium",
        "High"
    ],
    "Throw Distance": [
        "Short",
        "Medium",
        "Long",
        "Very Long"
    ]
})

st.dataframe(comparison_df)

# =========================
# CHARTS
# =========================

st.header("📈 HVAC Visualization")

chart_df = pd.DataFrame({
    "Parameter": [
        "CFM",
        "Velocity",
        "Noise",
        "Cooling Load"
    ],
    "Value": [
        cfm,
        velocity,
        noise,
        cooling_load
    ]
})

fig = px.bar(
    chart_df,
    x="Parameter",
    y="Value",
    color="Parameter",
    title="HVAC Performance Analysis"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# ENGINEERING EXPLANATION
# =========================

st.header("📘 Engineering Explanation")

st.write("""
### Airflow (CFM)
Represents the required amount of air supplied into the room.

### Velocity
Higher velocity increases air movement but may increase noise.

### Noise Criteria (NC)
Used to estimate indoor acoustic comfort.

### Cooling Load
Represents the required cooling capacity for the space.

### Diffuser Selection
Diffusers are selected based on airflow requirement and throw distance.
""")

# =========================
# PDF REPORT
# =========================

st.header("📄 Export Professional Report")

if st.button("Generate PDF Report"):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="AeroSelect Pro HVAC Report", ln=True)

    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Room Area: {room_area:.1f} ft²", ln=True)
    pdf.cell(200, 10, txt=f"Room Volume: {room_volume:.1f} ft³", ln=True)
    pdf.cell(200, 10, txt=f"Airflow: {cfm:.1f} CFM", ln=True)
    pdf.cell(200, 10, txt=f"Velocity: {velocity:.1f} FPM", ln=True)
    pdf.cell(200, 10, txt=f"Noise Level: {noise:.1f} NC", ln=True)
    pdf.cell(200, 10, txt=f"Cooling Load: {cooling_load:.1f} BTU/h", ln=True)
    pdf.cell(200, 10, txt=f"Recommended Diffuser: {recommended}", ln=True)

    pdf.output("HVAC_Report.pdf")

    with open("HVAC_Report.pdf", "rb") as file:

        st.download_button(
            label="⬇ Download PDF Report",
            data=file,
            file_name="HVAC_Report.pdf",
            mime="application/pdf"
        )

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption("Developed using Streamlit | AeroSelect Pro © 2026")