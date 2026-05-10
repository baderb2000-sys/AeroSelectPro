import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AeroSelect Pro",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("AeroSelect Pro")
st.subheader("HVAC Diffuser Selection Tool")

st.markdown("---")

# =========================
# SIDEBAR INPUTS
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

ceiling_height = st.sidebar.number_input(
    "Ceiling Height (ft)",
    min_value=1.0,
    value=10.0
)

occupancy = st.sidebar.selectbox(
    "Occupancy Type",
    ["Office", "Classroom", "Hospital", "Residential"]
)

total_cfm = st.sidebar.number_input(
    "Total Airflow (CFM)",
    min_value=100,
    value=2000
)

num_diffusers = st.sidebar.number_input(
    "Number of Diffusers",
    min_value=1,
    value=4
)

nc_limit = st.sidebar.number_input(
    "Maximum NC",
    min_value=10,
    value=30
)

# =========================
# TITUS DATA
# =========================

titus_data = pd.DataFrame({
    "Model": ["TMS-6", "TMS-8", "TMS-10", "TMS-12"],
    "Neck Size": ["6 in", "8 in", "10 in", "12 in"],
    "CFM": [150, 300, 500, 700],
    "Throw": [6, 10, 14, 18],
    "NC": [20, 25, 30, 35]
})

# =========================
# BUTTON
# =========================

if st.button("Calculate & Select Diffuser"):

    # =====================
    # CALCULATIONS
    # =====================

    cfm_per_diffuser = total_cfm / num_diffusers

    area = room_length * room_width

    characteristic_length = 1.06 * math.sqrt(area)

    required_throw = 0.75 * characteristic_length

    # =====================
    # SELECTION
    # =====================

    selected = None

    for index, row in titus_data.iterrows():

        if (
            row["CFM"] >= cfm_per_diffuser and
            row["Throw"] >= required_throw and
            row["NC"] <= nc_limit
        ):

            selected = row
            break

    # =====================
    # RESULTS
    # =====================

    col1, col2 = st.columns(2)

    with col1:

        st.header("Engineering Results")

        st.write(f"Room Area: {area:.2f} ft²")
        st.write(f"CFM per Diffuser: {cfm_per_diffuser:.2f} CFM")
        st.write(f"Characteristic Length (L): {characteristic_length:.2f} ft")
        st.write(f"Required Throw (X50): {required_throw:.2f} ft")

        if selected is not None:

            st.success("Suitable Diffuser Found")

            st.write(f"Selected Model: {selected['Model']}")
            st.write(f"Neck Size: {selected['Neck Size']}")
            st.write(f"Catalog Throw: {selected['Throw']} ft")
            st.write(f"Expected NC: {selected['NC']}")

            st.info(
                f"""
                The selected diffuser satisfies the airflow requirement
                while maintaining acceptable NC levels and sufficient throw.
                """
            )

        else:

            st.error("No suitable diffuser found.")

    # =====================
    # LAYOUT DRAWING
    # =====================

    with col2:

        st.header("Ceiling Layout")

        fig, ax = plt.subplots(figsize=(6, 6))

        # Room boundary
        ax.plot(
            [0, room_length, room_length, 0, 0],
            [0, 0, room_width, room_width, 0]
        )

        positions = []

        if num_diffusers == 1:

            positions = [
                (room_length / 2, room_width / 2)
            ]

        elif num_diffusers == 4:

            positions = [
                (room_length * 0.25, room_width * 0.25),
                (room_length * 0.75, room_width * 0.25),
                (room_length * 0.25, room_width * 0.75),
                (room_length * 0.75, room_width * 0.75)
            ]

        else:

            for i in range(int(num_diffusers)):

                x = room_length * (i + 1) / (num_diffusers + 1)
                y = room_width / 2

                positions.append((x, y))

        # Draw diffusers
        for i, (x, y) in enumerate(positions):

            ax.scatter(x, y, s=300)

            ax.text(
                x,
                y,
                f"D{i+1}",
                ha='center',
                va='center',
                color='white'
            )

        ax.set_xlim(-1, room_length + 1)
        ax.set_ylim(-1, room_width + 1)

        ax.set_aspect('equal')

        ax.grid(True)

        st.pyplot(fig)

    # =====================
    # TABLE
    # =====================

    st.header("Titus Manufacturer Data")

    st.dataframe(titus_data)

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption("AeroSelect Pro v1.0")