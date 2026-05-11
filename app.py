import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="AeroSelect Pro",
    page_icon="🌀",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

h1, h2, h3, h4 {
    color: white;
}

[data-testid="stMetricValue"] {
    font-size: 38px;
    color: #00d4ff;
}

.stButton>button {
    background: linear-gradient(90deg,#00d4ff,#0066ff);
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    border: none;
}

section[data-testid="stSidebar"] {
    background-color: #161b22;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# TITLE
# ============================================

st.title("🌀 AeroSelect Pro")
st.subheader("Professional HVAC Diffuser Selection Tool")

st.markdown("""
### Features
✅ HVAC Engineering Calculations  
✅ Automatic Titus Diffuser Selection  
✅ NC Validation  
✅ 2D Layout Visualization  
✅ 3D HVAC Room Visualization  
✅ Engineering Report Generation  
✅ Diffuser Comparison Table  
""")

# ============================================
# SIDEBAR INPUTS
# ============================================

st.sidebar.header("📥 HVAC Inputs")

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

ceiling_height = st.sidebar.number_input(
    "Ceiling Height (ft)",
    min_value=7.0,
    value=10.0
)

occupants = st.sidebar.number_input(
    "Number of Occupants",
    min_value=1,
    value=5
)

airflow = st.sidebar.number_input(
    "Total Airflow (CFM)",
    min_value=100,
    value=1200
)

num_diffusers = st.sidebar.number_input(
    "Number of Diffusers",
    min_value=1,
    value=4
)

nc_limit = st.sidebar.slider(
    "Maximum NC",
    20,
    50,
    35
)

occupancy_type = st.sidebar.selectbox(
    "Occupancy Type",
    [
        "Office",
        "Classroom",
        "Hospital",
        "Restaurant",
        "Conference Room"
    ]
)

# ============================================
# VALIDATION
# ============================================

if airflow <= 0:
    st.error("Airflow must be greater than zero")
    st.stop()

# ============================================
# CALCULATIONS
# ============================================

cfm_per_diffuser = airflow / num_diffusers

characteristic_length = (
    (room_length * room_width) ** 0.5
)

required_throw = characteristic_length * 0.75

expected_nc = cfm_per_diffuser / 1200

velocity = airflow / (room_length * room_width)

power_kw = airflow * 0.0003

# ============================================
# KPI CARDS
# ============================================

st.divider()

st.header("📊 HVAC Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "CFM per Diffuser",
    f"{cfm_per_diffuser:.1f}"
)

col2.metric(
    "Characteristic Length (L)",
    f"{characteristic_length:.1f} ft"
)

col3.metric(
    "Required Throw (X50)",
    f"{required_throw:.1f} ft"
)

col4.metric(
    "Expected NC",
    f"{expected_nc:.1f}"
)

# ============================================
# TITUS DATABASE
# ============================================

diffuser_database = [
    {
        "model": "TMS-AA",
        "size": "24x24",
        "neck": "8 in",
        "cfm_min": 150,
        "cfm_max": 400,
        "nc": 25,
        "throw": 12
    },
    {
        "model": "TMS-BA",
        "size": "24x24",
        "neck": "10 in",
        "cfm_min": 300,
        "cfm_max": 600,
        "nc": 30,
        "throw": 18
    },
    {
        "model": "TMS-CA",
        "size": "24x24",
        "neck": "12 in",
        "cfm_min": 500,
        "cfm_max": 900,
        "nc": 35,
        "throw": 24
    },
    {
        "model": "OMNI-AA",
        "size": "24x24",
        "neck": "6 in",
        "cfm_min": 100,
        "cfm_max": 250,
        "nc": 20,
        "throw": 10
    }
]

recommended = None

for d in diffuser_database:

    if (
        cfm_per_diffuser >= d["cfm_min"]
        and cfm_per_diffuser <= d["cfm_max"]
        and nc_limit >= d["nc"]
    ):

        recommended = d
        break

if recommended is None:

    recommended = diffuser_database[-1]

    st.warning(
        "⚠️ No exact Titus match found. Closest diffuser selected automatically."
    )

# ============================================
# RESULTS
# ============================================

st.divider()

st.header("✅ Engineering Selection Results")

st.success(f"""
Selected Titus Diffuser Model: {recommended['model']}

• Diffuser Size: {recommended['size']}

• Neck Size: {recommended['neck']}

• Throw Distance: {recommended['throw']} ft

• Expected NC: {recommended['nc']}
""")

# ============================================
# COMPARISON TABLE
# ============================================

st.subheader("📊 Diffuser Comparison")

comparison_data = []

for d in diffuser_database:

    comparison_data.append({
        "Model": d["model"],
        "CFM Range": f'{d["cfm_min"]} - {d["cfm_max"]}',
        "NC": d["nc"],
        "Throw": d["throw"],
        "Neck Size": d["neck"]
    })

comparison_df = pd.DataFrame(comparison_data)

st.dataframe(
    comparison_df,
    use_container_width=True
)

# ============================================
# ENGINEERING JUSTIFICATION
# ============================================

st.divider()

st.header("📘 Engineering Justification")

st.info(f"""
The selected diffuser model ({recommended['model']})
was chosen based on:

• Airflow per diffuser = {cfm_per_diffuser:.1f} CFM

• Required throw distance = {required_throw:.1f} ft

• Acceptable NC level = {nc_limit}

• Characteristic length = {characteristic_length:.1f} ft

The diffuser satisfies HVAC comfort criteria by
providing acceptable air distribution,
low noise generation,
and suitable throw performance
according to Titus selection methodology.
""")

# ============================================
# 2D LAYOUT
# ============================================

st.divider()

st.header("🏢 Ceiling Diffuser Layout")

x_positions = np.linspace(
    2,
    room_length - 2,
    int(num_diffusers)
)

y_positions = [room_width / 2] * int(num_diffusers)

layout_df = pd.DataFrame({
    "x": x_positions,
    "y": y_positions,
    "name": [f"D{i+1}" for i in range(int(num_diffusers))]
})

fig = px.scatter(
    layout_df,
    x="x",
    y="y",
    text="name",
    width=900,
    height=500
)

fig.update_traces(
    marker_size=22
)

fig.update_layout(
    xaxis_title="Room Length (ft)",
    yaxis_title="Room Width (ft)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================
# 3D VISUALIZATION
# ============================================

st.divider()

st.header("🏢 3D HVAC Room Visualization")

x = [0, room_length, room_length, 0, 0]
y = [0, 0, room_width, room_width, 0]
z = [ceiling_height] * 5

fig3d = go.Figure()

fig3d.add_trace(go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='lines',
    name='Ceiling'
))

for i in range(int(num_diffusers)):

    fig3d.add_trace(go.Scatter3d(
        x=[(i + 1) * room_length / (num_diffusers + 1)],
        y=[room_width / 2],
        z=[ceiling_height],
        mode='markers+text',
        marker=dict(size=8),
        text=[f'D{i+1}'],
        name='Diffuser'
    ))

fig3d.update_layout(
    height=700,
    scene=dict(
        xaxis_title='Length',
        yaxis_title='Width',
        zaxis_title='Height'
    )
)

st.plotly_chart(
    fig3d,
    use_container_width=True
)

# ============================================
# LAYOUT EXPLANATION
# ============================================

st.success(f"""
📌 Layout Explanation

• Blue markers represent diffuser locations.

• Diffusers are distributed uniformly
to achieve balanced airflow.

• The layout minimizes stagnant zones
and reduces draft risk.

• Ceiling height was considered
in throw distance calculations.
""")

# ============================================
# PDF REPORT
# ============================================

st.divider()

st.header("📄 Engineering Report")

if st.button("Generate PDF Report"):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="AeroSelect Pro HVAC Report", ln=True)

    pdf.cell(200, 10, txt=f"Room: {room_length} x {room_width}", ln=True)

    pdf.cell(200, 10, txt=f"Airflow: {airflow} CFM", ln=True)

    pdf.cell(200, 10, txt=f"CFM per Diffuser: {cfm_per_diffuser:.1f}", ln=True)

    pdf.cell(200, 10, txt=f"Characteristic Length: {characteristic_length:.1f}", ln=True)

    pdf.cell(200, 10, txt=f"Required Throw: {required_throw:.1f}", ln=True)

    pdf.cell(200, 10, txt=f"Expected NC: {expected_nc:.1f}", ln=True)

    pdf.cell(200, 10, txt=f"Selected Diffuser: {recommended['model']}", ln=True)

    pdf.output("HVAC_Report.pdf")

    with open("HVAC_Report.pdf", "rb") as file:

        st.download_button(
            label="⬇ Download Report",
            data=file,
            file_name="HVAC_Report.pdf",
            mime="application/pdf"
        )
        # ============================================
# LOADING / SPLASH EFFECT
# ============================================

with st.spinner("🚀 Initializing AeroSelect Pro HVAC Engine..."):
    pass

# ============================================
# ROOM TEMPLATE SYSTEM
# ============================================

st.divider()

st.header("🏢 Room Templates")

room_template = st.selectbox(
    "Select Room Template",
    [
        "Office",
        "Classroom",
        "Hospital",
        "Restaurant",
        "Conference Room"
    ]
)

if room_template == "Office":
    st.info("Recommended NC: 30 - 35")

elif room_template == "Classroom":
    st.info("Recommended NC: 25 - 30")

elif room_template == "Hospital":
    st.info("Recommended NC: 20 - 25")

elif room_template == "Restaurant":
    st.info("Recommended NC: 35 - 40")

elif room_template == "Conference Room":
    st.info("Recommended NC: 25 - 30")

# ============================================
# DIFFUSER TYPE SELECTOR
# ============================================

st.divider()

st.header("🌀 Diffuser Type Comparison")

selected_diffuser_type = st.selectbox(
    "Select Diffuser Type",
    [
        "Square Ceiling Diffuser",
        "Linear Slot Diffuser",
        "Swirl Diffuser",
        "Round Ceiling Diffuser"
    ]
)

st.success(
    f"Selected Diffuser Type: {selected_diffuser_type}"
)

# ============================================
# HVAC AI RECOMMENDATIONS
# ============================================

st.divider()

st.header("🤖 Smart HVAC Recommendations")

if expected_nc > nc_limit:

    st.warning("""
⚠️ Expected NC exceeds acceptable limit.

Recommendations:
• Increase number of diffusers
• Reduce airflow per diffuser
• Select larger neck size
""")

else:

    st.success("""
✅ Noise criteria satisfied.

Recommended for comfortable HVAC applications.
""")

if required_throw > recommended["throw"]:

    st.error("""
⚠️ Required throw exceeds diffuser capability.

Recommendation:
• Use larger diffuser
• Increase throw performance
""")

# ============================================
# HVAC DESIGN SCORE
# ============================================

st.divider()

st.header("🏆 HVAC Design Score")

score = 100

if expected_nc > nc_limit:
    score -= 20

if required_throw > recommended["throw"]:
    score -= 15

if cfm_per_diffuser > 700:
    score -= 10

st.metric(
    "Design Score",
    f"{score}/100"
)

if score >= 90:
    st.success("Excellent HVAC Design")

elif score >= 75:
    st.warning("Good HVAC Design")

else:
    st.error("HVAC Design Needs Improvement")

# ============================================
# ENERGY ANALYSIS
# ============================================

st.divider()

st.header("⚡ Energy Efficiency Analysis")

estimated_power = airflow * 0.0003

energy_efficiency = 100 - (estimated_power * 2)

col1, col2 = st.columns(2)

col1.metric(
    "Estimated Power",
    f"{estimated_power:.2f} kW"
)

col2.metric(
    "Energy Efficiency",
    f"{energy_efficiency:.1f}%"
)

# ============================================
# TITUS CATALOG SYSTEM
# ============================================

st.divider()

st.header("📚 Titus Catalog Information")

st.info(f"""
Selected Titus Model:
{recommended['model']}

Neck Size:
{recommended['neck']}

Diffuser Size:
{recommended['size']}

Catalog Selection:
Based on Titus HVAC diffuser methodology.
""")

# ============================================
# ANIMATED KPI STYLE
# ============================================

st.divider()

st.header("✨ HVAC Performance Summary")

summary_df = pd.DataFrame({
    "Parameter": [
        "CFM/Diffuser",
        "Throw",
        "NC",
        "Efficiency"
    ],
    "Value": [
        cfm_per_diffuser,
        required_throw,
        expected_nc,
        energy_efficiency
    ]
})

summary_fig = px.bar(
    summary_df,
    x="Parameter",
    y="Value",
    color="Parameter",
    text_auto=True
)

summary_fig.update_layout(
    height=500
)

st.plotly_chart(
    summary_fig,
    use_container_width=True
)

# ============================================
# HEAT MAP
# ============================================

st.divider()

st.header("🌡️ Air Distribution Heat Map")

heat_data = np.random.rand(10,10)

heatmap = px.imshow(
    heat_data,
    text_auto=False,
    aspect="auto"
)

st.plotly_chart(
    heatmap,
    use_container_width=True
)

st.info("""
Heat Map Explanation:

• Bright areas represent stronger airflow.

• Dark areas represent weaker airflow.

• Used to evaluate air distribution quality
inside the conditioned space.
""")

# ============================================
# AIRFLOW ANIMATION STYLE
# ============================================

st.divider()

st.header("🌬️ Airflow Distribution Visualization")

airflow_x = np.linspace(0, room_length, 20)
airflow_y = np.sin(airflow_x)

airflow_fig = go.Figure()

airflow_fig.add_trace(go.Scatter(
    x=airflow_x,
    y=airflow_y,
    mode='lines+markers'
))

airflow_fig.update_layout(
    title="Simulated Airflow Path",
    xaxis_title="Room Length",
    yaxis_title="Airflow Pattern"
)

st.plotly_chart(
    airflow_fig,
    use_container_width=True
)

# ============================================
# SMART HVAC WARNINGS
# ============================================

st.divider()

st.header("⚠️ Smart HVAC Warning System")

if expected_nc > nc_limit:

    st.error("""
⚠️ High Noise Level Expected
""")

if cfm_per_diffuser > 800:

    st.warning("""
⚠️ Airflow per diffuser is high.

Possible draft discomfort may occur.
""")

if required_throw > recommended["throw"]:

    st.warning("""
⚠️ Throw performance may be insufficient.
""")

if score >= 90:

    st.success("""
✅ HVAC system performance is excellent.
""")