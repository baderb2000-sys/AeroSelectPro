import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AeroSelect Pro Ultra",
    page_icon="🌬️",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1,h2,h3 {
    color: #4FC3F7;
}

[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================

st.title("🌬️ AeroSelect Pro Ultra")
st.subheader("AI-Powered HVAC Engineering Platform")

st.markdown("---")

# =====================================
# SIDEBAR INPUTS
# =====================================

st.sidebar.header("HVAC Inputs")

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

occupancy = st.sidebar.number_input(
    "Occupancy",
    min_value=1,
    value=10
)

system_type = st.sidebar.selectbox(
    "HVAC System",
    [
        "AHU + Diffuser",
        "FCU + Diffuser",
        "VAV System",
        "Jet Ventilation"
    ]
)

# =====================================
# VALIDATION
# =====================================

if room_length <= 0 or room_width <= 0 or room_height <= 0:
    st.error("❌ Invalid room dimensions")
    st.stop()

# =====================================
# CALCULATIONS
# =====================================

room_volume = room_length * room_width * room_height

required_cfm = room_volume / 2 + occupancy * 20

velocity = required_cfm / 100

noise = velocity * 1.4

power_kw = required_cfm / 500

monthly_energy = power_kw * 8 * 30

estimated_cost = monthly_energy * 0.18

# =====================================
# AI RECOMMENDATION
# =====================================

if required_cfm < 300:
    diffuser = "Ceiling Diffuser"

elif required_cfm < 700:
    diffuser = "Linear Slot"

elif required_cfm < 1200:
    diffuser = "Swirl Diffuser"

else:
    diffuser = "Jet Nozzle"

# =====================================
# KPI DASHBOARD
# =====================================

st.header("📊 HVAC Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Required CFM", f"{required_cfm:.1f}")

with col2:
    st.metric("Velocity", f"{velocity:.1f} FPM")

with col3:
    st.metric("Noise", f"{noise:.1f} NC")

with col4:
    st.metric("Power", f"{power_kw:.1f} kW")

# =====================================
# ENERGY SECTION
# =====================================

st.header("⚡ Energy Analysis")

energy_df = pd.DataFrame({
    "Parameter": [
        "Power (kW)",
        "Monthly Energy (kWh)",
        "Estimated Cost ($)"
    ],
    "Value": [
        power_kw,
        monthly_energy,
        estimated_cost
    ]
})

st.dataframe(energy_df, use_container_width=True)

# =====================================
# 3D ROOM VISUALIZATION
# =====================================

st.header("🏢 3D Room Visualization")

x = [0, room_length, room_length, 0, 0]
y = [0, 0, room_width, room_width, 0]
z = [0, 0, 0, 0, 0]

fig3d = go.Figure(data=[
    go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='lines',
        line=dict(width=6)
    )
])

fig3d.update_layout(
    scene=dict(
        xaxis_title='Length',
        yaxis_title='Width',
        zaxis_title='Height'
    ),
    height=500
)

st.plotly_chart(fig3d, use_container_width=True)

# =====================================
# HEATMAP
# =====================================

st.header("🔥 Air Distribution Heatmap")

heat_data = np.random.rand(10, 10) * velocity

heatmap = px.imshow(
    heat_data,
    color_continuous_scale='Blues',
    title='Airflow Distribution'
)

st.plotly_chart(heatmap, use_container_width=True)

# =====================================
# CFD STYLE SIMULATION
# =====================================

st.header("🌪️ CFD Style Airflow Simulation")

x = np.linspace(0, room_length, 20)
y = np.linspace(0, room_width, 20)

X, Y = np.meshgrid(x, y)

U = np.cos(X / 2)
V = np.sin(Y / 2)

cfd_fig = go.Figure(data=go.Cone(
    x=X.flatten(),
    y=Y.flatten(),
    z=np.zeros_like(X.flatten()),
    u=U.flatten(),
    v=V.flatten(),
    w=np.ones_like(U.flatten()) * 0.2,
    sizemode="absolute",
    sizeref=2
))

cfd_fig.update_layout(height=700)

st.plotly_chart(cfd_fig, use_container_width=True)

# =====================================
# AI RESULT
# =====================================

st.success(f"✅ AI Recommended Diffuser: {diffuser}")

# =====================================
# SYSTEM SUMMARY
# =====================================

st.header("📋 HVAC System Summary")

summary_df = pd.DataFrame({
    "Parameter": [
        "System Type",
        "Recommended Diffuser",
        "Room Volume",
        "Required CFM",
        "Velocity",
        "Noise"
    ],
    "Value": [
        system_type,
        diffuser,
        room_volume,
        required_cfm,
        velocity,
        noise
    ]
})

st.table(summary_df)

# =====================================
# PDF REPORT
# =====================================

if st.button("📄 Generate HVAC Report"):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="AeroSelect Pro Ultra Report", ln=True)

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Room Volume: {room_volume:.1f}", ln=True)
    pdf.cell(200, 10, txt=f"Required CFM: {required_cfm:.1f}", ln=True)
    pdf.cell(200, 10, txt=f"Velocity: {velocity:.1f}", ln=True)
    pdf.cell(200, 10, txt=f"Noise: {noise:.1f}", ln=True)
    pdf.cell(200, 10, txt=f"Power: {power_kw:.1f} kW", ln=True)
    pdf.cell(200, 10, txt=f"Recommended Diffuser: {diffuser}", ln=True)

    pdf.output("HVAC_Report.pdf")

    with open("HVAC_Report.pdf", "rb") as file:

        st.download_button(
            label="⬇ Download Report",
            data=file,
            file_name="HVAC_Report.pdf",
            mime="application/pdf"
        )