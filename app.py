import streamlit as st
import pandas as pd
import joblib
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Import helper modules
from propulsion_physics import (
    fuel_curve,
    resistance_increase,
    power_required,
    speed_loss_due_to_fouling,
    fuel_consumption_tph
)

from safety_rules import check_operational_safety
from maintenance_schedule import maintenance_action
from hull3d import hull_3d_figure
from hull3d_fouled import hull_fouled_figure

# Load the model
model = joblib.load("biofouling_model.pkl")

# App Title
st.title("🚢 Ship Hull Biofouling Prediction & Hull Performance Optimization")

st.write("""
This app predicts **biofouling severity** using logistic regression,
and provides **maintenance and safety recommendations**.
""")

# Inputs
vessel_speed = st.slider("Vessel Speed (kn)", 6, 20, 12)
idle_days = st.number_input("Idle Days", 2, 25, 10)
temp = st.slider("Sea Temperature (°C)", 19, 35, 28)
salinity = st.slider("Salinity (ppt)", 30, 40, 35)
days_since_clean = st.number_input("Days Since Last Cleaning", 0, 80, 60)
roughness = st.slider("Hull Roughness (mm)", 0.01, 0.221, 0.05)
# REMOVE friction slider OR keep it but override it
# friction = st.slider("Friction Coefficient", 0.00113, 0.00437, 0.002)
# Automatically calculate friction based on roughness
friction = 0.002 + roughness * 0.02
fuel_penalty = st.slider("Fuel Penalty (%)", 2, 27, 5)

# Prediction
input_data = pd.DataFrame({
    "sea_temperature": [temp],
    "salinity": [salinity],
    "idle_days": [idle_days],
    "avg_speed": [vessel_speed],
    "days_since_cleaning": [days_since_clean],
    "hull_roughness": [roughness],
    "friction_coeff": [friction],
    "fuel_penalty": [fuel_penalty]
})

prediction = model.predict(input_data)[0]

probs = model.predict_proba(input_data)[0]
st.write("Prediction Probabilities:", probs)

st.subheader("📌 Prediction Result")
severity_map = {
    0: ("🟢 LOW", "green"),
    1: ("🟠 MODERATE", "orange"),
    2: ("🔴 SEVERE", "red")
}

label, color = severity_map[prediction]

st.markdown(
    f"<h3 style='color:{color}'>Biofouling Severity: {label}</h3>",
    unsafe_allow_html=True
)

# Safety + Maintenance
safety_message = check_operational_safety(vessel_speed, roughness, days_since_clean)
st.write(safety_message)

maintenance_message = maintenance_action(prediction)
st.write(maintenance_message)

# Performance Metrics
res = resistance_increase(roughness, vessel_speed)
power_kw = power_required(res, vessel_speed) / 1000
speed_loss = speed_loss_due_to_fouling(roughness, vessel_speed)
fuel_tph = fuel_consumption_tph(power_kw)

st.subheader("📈 Hull Performance Metrics")
st.write(f"Resistance (N): {res:.2f}")
st.write(f"Power Required (kW): {power_kw:.2f}")
st.write(f"Speed after Fouling (kn): {speed_loss:.2f}")
st.write(f"Fuel Consumption (t/hr): {fuel_tph:.4f}")

# Plot chart
st.subheader("📉 Vessel Speed Loss vs Hull Fouling")
roughness_range = np.linspace(0.01, 0.2, 30)
speed_after_fouling = [
    speed_loss_due_to_fouling(r, vessel_speed) for r in roughness_range
]
speed_df = pd.DataFrame({
    "Hull Roughness (mm)": roughness_range,
    "Speed After Fouling (kn)": speed_after_fouling
})
speed_chart = alt.Chart(speed_df).mark_line(point=True).encode(
    x=alt.X("Hull Roughness (mm)", title="Hull Roughness (mm)"),
    y=alt.Y("Speed After Fouling (kn)", title="Speed (kn)")
).properties(
    height=400
)
st.altair_chart(speed_chart, use_container_width=True)

# Remove any invalid rows
speed_df = speed_df.dropna()

# Fuel Consumption vs Hull Fouling Chart
fouling_range = np.linspace(0.01, 0.2, 50)
fuel_values = [
    fuel_consumption_tph(power_required(resistance_increase(r, vessel_speed), vessel_speed) / 1000)
    for r in fouling_range
]

df_fuel = pd.DataFrame({
    "Hull Roughness (mm)": fouling_range,
    "Fuel Consumption (t/hr)": fuel_values
})

fuel_chart = alt.Chart(df_fuel).mark_line(point=True).encode(
    x=alt.X("Hull Roughness (mm)", title="Hull Roughness (mm)"),
    y=alt.Y("Fuel Consumption (t/hr)", title="Fuel Consumption (t/hr)")
).properties(
    height=400,
    title="📊 Fuel Consumption vs Hull Fouling"
)

st.altair_chart(fuel_chart, use_container_width=True)

st.subheader("🧭 3D Ship Hull Visualization")
# Display the 3D plotly figure from hull3d.py
st.plotly_chart(hull_3d_figure(), use_container_width=True)

st.subheader("🛳️ Fouled Hull Visualization")
t = st.slider("Fouling level (0 = clean, 1 = heavy)", 0.0, 1.0, 0.7)
fig = hull_fouled_figure(t=t)
st.plotly_chart(fig, use_container_width=True)
