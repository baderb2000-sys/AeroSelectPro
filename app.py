import streamlit as st
import pandas as pd
import plotly.express as px
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

h1,h2,h3,h4 {
    color: #00FFF5;
}

.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}

[data-testid="metric-container"] {
    background-color: #1B1F2A;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 0px 12px rgba(0,255,255,0.2);
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("❄️ AeroSelect Pro")
st.subheader("Professional HVAC Diffuser Selection Tool")

st.markdown("""
AeroSelect Pro is an advanced HVAC engineering tool designed for:

✅ Diffuser Selection  
✅ HVAC Calculations  
✅ Cooling Load Estimation  
✅ Noise Analysis  
✅ Airflow Optimization  
✅ Professional Engineering Reports  
""")

st.markdown("---")

# =========================
# SIDEBAR
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
    "Number of Occupants",
    min_value=1,
    value=5
)

building_type = st.sidebar.selectbox(
    "Building Type",
    [
        "Office",
        "Classroom",
        "Hospital",
        "Restaurant",
        "Residential"
    ]
)

noise_target = st.sidebar.slider(
    "Target Noise Level (NC)",
    20,
    60,
    35
)

temperature = st.sidebar.slider(
    "Room Temperature (°C)",
    16,
    35,
    24
)

diffuser = st.sidebar.selectbox(
    "Diffuser Type",
    [
        "Ceiling Diffuser",
        "Linear Diffuser",
        "Slot Diffuser",
        "Swirl Diffuser",
        "Jet Diffuser"
    ]
)

# =========================
# VALIDATION
# =========================

if room_length <= 0 or room_width <= 0 or room_height <= 0:
    st.error("❌ Invalid room dimensions")
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

ach = (cfm * 60) / room_volume

throw_distance = velocity * 0.8

static_pressure = velocity * 0.05

# =========================
# AUTO RECOMMENDATION
# =========================

if cfm < 300:
    recommendation = "Ceiling Diffuser"

elif cfm < 500:
    recommendation = "Linear Diffuser"

elif cfm < 800:
    recommendation = "Swirl Diffuser"

else:
    recommendation = "Jet Diffuser"

# =========================
# KPI CARDS
# =========================

st.header("📊 HVAC KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Airflow", f"{cfm:.1f} CFM")

with col2:
    st.metric("Velocity", f"{velocity:.1f} FPM")

with col3:
    st.metric("Noise", f"{noise:.1f} NC")

with col4:
    st.metric("Cooling Load", f"{cooling_load:.1f} BTU/h")

# =========================
# ENGINEERING RESULTS
# =========================

st.markdown("---")

st.header("📌 Engineering Results")

st.success(f"✅ Recommended Diffuser: {recommendation}")

results_df = pd.DataFrame({
    "Parameter": [
        "Room Area",
        "Room Volume",
        "Airflow",
        "Velocity",
        "Noise",
        "Cooling Load",
        "Power",
        "ACH",
        "Throw Distance",
        "Static Pressure"
    ],
    "Value": [
        f"{room_area:.1f} ft²",
        f"{room_volume:.1f} ft³",
        f"{cfm:.1f} CFM",
        f"{velocity:.1f} FPM",
        f"{noise:.1f} NC",
        f"{cooling_load:.1f} BTU/h",
        f"{power_kw:.2f} kW",
        f"{ach:.2f}",
        f"{throw_distance:.1f} ft",
        f"{static_pressure:.2f} in.wg"
    ]
})

st.dataframe(results_df)

# =========================
# DIFFUSER COMPARISON
# =========================

st.header("📋 Diffuser Comparison")

comparison = pd.DataFrame({
    "Diffuser": [
        "Ceiling",
        "Linear",
        "Swirl",
        "Jet"
    ],
    "Airflow": [
        "100-300",
        "300-500",
        "500-800",
        "800+"
    ],
    "Noise": [
        "Low",
        "Medium",
        "Medium",
        "High"
    ],
    "Throw": [
        "Short",
        "Medium",
        "Long",
        "Very Long"
    ]
})

st.table(comparison)

# =========================
# CHARTS
# =========================

st.header("📈 HVAC Performance Charts")

chart_df = pd.DataFrame({
    "Parameter": [
        "CFM",
        "Velocity",
        "Noise",
        "Cooling Load",
        "ACH"
    ],
    "Value": [
        cfm,
        velocity,
        noise,
        cooling_load,
        ach
    ]
})

fig = px.bar(
    chart_df,
    x="Parameter",
    y="Value",
    color="Parameter",
    title="HVAC Analysis"
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
This chart visualizes HVAC performance indicators.

- Higher airflow improves ventilation.
- Excessive velocity may increase noise.
- Cooling load affects HVAC equipment sizing.
""")

# =========================
# HVAC NOTES
# =========================

st.header("📘 HVAC Engineering Notes")

st.write("""
### Airflow (CFM)
Represents the amount of conditioned air supplied into the space.

### Velocity
Air velocity affects comfort and diffuser performance.

### ACH
Air Changes per Hour indicates ventilation effectiveness.

### Cooling Load
Represents total required cooling capacity.

### Static Pressure
Pressure losses through ducts and diffusers.
""")

# =========================
# EXPORT CSV
# =========================

csv = results_df.to_csv(index=False)

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="HVAC_Data.csv",
    mime="text/csv"
)

# =========================
# PDF REPORT
# =========================

st.header("📄 Generate PDF Report")

if st.button("Create PDF Report"):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="AeroSelect Pro HVAC Report", ln=True)

    pdf.ln(10)

    for i in range(len(results_df)):
        pdf.cell(
            200,
            10,
            txt=f"{results_df.iloc[i,0]} : {results_df.iloc[i,1]}",
            ln=True
        )

    pdf.output("HVAC_Report.pdf")

    with open("HVAC_Report.pdf", "rb") as file:

        st.download_button(
            label="⬇ Download PDF",
            data=file,
            file_name="HVAC_Report.pdf",
            mime="application/pdf"
        )

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption("AeroSelect Pro © 2026 | Professional HVAC Engineering Application")