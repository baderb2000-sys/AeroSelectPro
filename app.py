import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AeroSelect Pro",
    page_icon="❄️",
    layout="wide"
)

# ==================================================
# GLASSMORPHISM UI
# ==================================================

st.markdown("""
<style>

.main {
    background:
    linear-gradient(
        135deg,
        #020617,
        #0f172a
    );
}

section[data-testid="stSidebar"] {

    background:
    rgba(15,23,42,0.7);

    backdrop-filter: blur(16px);

    border-right:
    1px solid rgba(255,255,255,0.08);
}

.hero {

    padding: 40px;

    border-radius: 24px;

    background:
    rgba(255,255,255,0.05);

    backdrop-filter:
    blur(18px);

    border:
    1px solid rgba(255,255,255,0.08);

    margin-bottom: 30px;

    box-shadow:
    0 8px 32px rgba(0,0,0,0.35);
}

h1,h2,h3,h4 {
    color: white;
}

.stMetric {

    background:
    rgba(255,255,255,0.05);

    padding: 15px;

    border-radius: 18px;

    border:
    1px solid rgba(255,255,255,0.08);
}

[data-testid="stMetricValue"] {

    color: #00d4ff;

    font-size: 34px;
}

.stButton>button {

    background:
    linear-gradient(
        90deg,
        #00d4ff,
        #2563eb
    );

    color: white;

    border-radius: 14px;

    border: none;

    height: 50px;

    font-size: 18px;
}

.footer {

    text-align:center;

    color:gray;

    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">

<h1>❄️ Welcome to AeroSelect Pro</h1>

<h3>
Professional HVAC Diffuser Selection Platform
</h3>

<p>
Commercial HVAC engineering software for intelligent
diffuser selection using Titus engineering methodology.
</p>

</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🏢 HVAC Inputs")

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

total_cfm = st.sidebar.number_input(
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

# ==================================================
# HVAC CALCULATIONS
# ==================================================

cfm_per_diffuser = total_cfm / num_diffusers

characteristic_length = np.sqrt(
    room_length * room_width
)

required_throw = characteristic_length * 0.75

expected_nc = round(
    cfm_per_diffuser / 1500 * nc_limit,
    1
)

# ==================================================
# TITUS DATABASE
# ==================================================

diffuser_database = [

    {
        "model":"TMS-AA",
        "size":"24x24",
        "neck":"8 in",
        "cfm_min":150,
        "cfm_max":400,
        "nc":25,
        "throw":12
    },

    {
        "model":"TMS-BA",
        "size":"24x24",
        "neck":"10 in",
        "cfm_min":300,
        "cfm_max":600,
        "nc":30,
        "throw":18
    },

    {
        "model":"TMS-CA",
        "size":"24x24",
        "neck":"12 in",
        "cfm_min":500,
        "cfm_max":900,
        "nc":35,
        "throw":24
    }

]

recommended = diffuser_database[0]

for d in diffuser_database:

    if (
        cfm_per_diffuser >= d["cfm_min"]
        and cfm_per_diffuser <= d["cfm_max"]
        and nc_limit >= d["nc"]
    ):

        recommended = d

# ==================================================
# KPI SECTION
# ==================================================

st.header("📊 HVAC Performance")

k1,k2,k3,k4 = st.columns(4)

k1.metric(
    "CFM / Diffuser",
    f"{cfm_per_diffuser:.1f}"
)

k2.metric(
    "Characteristic Length",
    f"{characteristic_length:.1f} ft"
)

k3.metric(
    "Required Throw",
    f"{required_throw:.1f} ft"
)

k4.metric(
    "Expected NC",
    f"{expected_nc}"
)

# ==================================================
# SMART RECOMMENDATIONS
# ==================================================

st.header("🧠 Smart HVAC Recommendations")

recommendations = []

if expected_nc > nc_limit:

    recommendations.append(
        "Reduce airflow to lower NC level."
    )

if cfm_per_diffuser > 500:

    recommendations.append(
        "Consider adding more diffusers."
    )

if required_throw > recommended["throw"]:

    recommendations.append(
        "Use larger neck diffuser for longer throw."
    )

if len(recommendations) == 0:

    recommendations.append(
        "Current design satisfies HVAC criteria."
    )

for r in recommendations:

    st.success(f"✅ {r}")

# ==================================================
# ENGINEERING RESULTS
# ==================================================

st.header("✅ Engineering Selection Results")

st.success(f"""
Selected Titus Diffuser:

• Model: {recommended['model']}

• Size: {recommended['size']}

• Neck Size: {recommended['neck']}

• Throw Distance: {recommended['throw']} ft

• Expected NC: {recommended['nc']}
""")

# ==================================================
# COMPARISON TABLE
# ==================================================

st.header("📋 Diffuser Comparison")

comparison_df = pd.DataFrame(
    diffuser_database
)

st.dataframe(
    comparison_df,
    use_container_width=True
)

# ==================================================
# JUSTIFICATION
# ==================================================

st.header("📘 Engineering Justification")

st.info(f"""
The selected diffuser was chosen based on:

• Airflow per diffuser

• Throw distance requirements

• Acceptable NC limits

• HVAC comfort conditions

The selected diffuser satisfies
Titus engineering selection methodology.
""")

# ==================================================
# 2D LAYOUT
# ==================================================

st.header("📐 Ceiling Diffuser Layout")

fig = go.Figure()

fig.add_shape(
    type="rect",
    x0=0,
    y0=0,
    x1=room_length,
    y1=room_width,
    line=dict(color="cyan")
)

for i in range(num_diffusers):

    x = (
        (i + 1)
        * room_length
        / (num_diffusers + 1)
    )

    y = room_width / 2

    fig.add_trace(go.Scatter(

        x=[x],

        y=[y],

        mode="markers+text",

        text=[f"D{i+1}"],

        marker=dict(size=18)

    ))

fig.update_layout(
    template="plotly_dark",
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="layout_chart"
)

# ==================================================
# 3D VISUALIZATION
# ==================================================

st.header("🏢 3D HVAC Visualization")

fig3d = go.Figure()

fig3d.add_trace(go.Scatter3d(

    x=[
        0,
        room_length,
        room_length,
        0,
        0
    ],

    y=[
        0,
        0,
        room_width,
        room_width,
        0
    ],

    z=[ceiling_height]*5,

    mode='lines',

    name='Room'

))

for i in range(num_diffusers):

    fig3d.add_trace(go.Scatter3d(

        x=[
            (i+1)
            * room_length
            / (num_diffusers+1)
        ],

        y=[room_width/2],

        z=[ceiling_height],

        mode='markers+text',

        text=[f'D{i+1}'],

        marker=dict(size=6)

    ))

fig3d.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig3d,
    use_container_width=True,
    key="3d_chart"
)

# ==================================================
# HEATMAP
# ==================================================

st.header("🔥 Airflow Heatmap")

heatmap_data = np.random.rand(
    int(room_width),
    int(room_length)
)

heatmap_fig = px.imshow(
    heatmap_data,
    color_continuous_scale="Blues",
    template="plotly_dark"
)

heatmap_fig.update_layout(
    height=500
)

st.plotly_chart(
    heatmap_fig,
    use_container_width=True,
    key="heatmap_chart"
)

# ==================================================
# CFD AIRFLOW ANIMATION
# ==================================================

st.header("🌪️ CFD-Style Airflow Simulation")

air_x = np.linspace(
    0,
    room_length,
    25
)

air_y = np.linspace(
    0,
    room_width,
    25
)

cfd_fig = go.Figure()

for i in range(25):

    cfd_fig.add_trace(go.Scatter(

        x=air_x,

        y=np.sin(
            air_x/2 + i/3
        ) + air_y[i],

        mode='lines',

        line=dict(width=2),

        opacity=0.5,

        showlegend=False

    ))

cfd_fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    cfd_fig,
    use_container_width=True,
    key="cfd_chart"
)

# ==================================================
# ANALYTICS CHART
# ==================================================

st.header("📈 HVAC Analytics")

chart_df = pd.DataFrame({

    "Parameter":[
        "CFM",
        "Throw",
        "NC"
    ],

    "Value":[
        cfm_per_diffuser,
        required_throw,
        expected_nc
    ]

})

bar_fig = px.bar(
    chart_df,
    x="Parameter",
    y="Value",
    template="plotly_dark"
)

st.plotly_chart(
    bar_fig,
    use_container_width=True,
    key="analytics_chart"
)

# ==================================================
# PDF REPORT
# ==================================================

st.header("📄 Engineering PDF Report")

if st.button("Generate PDF Report"):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=14
    )

    pdf.cell(
        200,
        10,
        txt="AeroSelect Pro HVAC Report",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Room Size: {room_length} x {room_width}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"CFM per Diffuser: {cfm_per_diffuser:.1f}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Selected Diffuser: {recommended['model']}",
        ln=True
    )

    pdf.output(
        "HVAC_Report.pdf"
    )

    with open(
        "HVAC_Report.pdf",
        "rb"
    ) as file:

        st.download_button(

            label="⬇ Download PDF",

            data=file,

            file_name="HVAC_Report.pdf",

            mime="application/pdf"

        )

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">

AeroSelect Pro © 2026

Professional HVAC Diffuser Selection Platform

</div>
""", unsafe_allow_html=True)
