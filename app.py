import streamlit as st
import pandas as pd
import joblib
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

def speed_loss_due_to_fouling(roughness, vessel_speed):
    loss_percent = roughness * 50
    # Prevent negative speed
    if loss_percent >= 100:
        loss_percent = 99
    return vessel_speed_kn * (1 - loss_percent / 100)

# Import helper modules
from propulsion_physics import (
    fuel_curve,
    resistance_increase,
    power_required,
    speed_loss_due_to_fouling,
    fuel_consumption
)

from safety_rules import check_operational_safety
from maintenance_schedule import maintenance_action

# Load the model
model = joblib.load("biofouling_model.pkl")

# App Title
st.title("🚢 Ship Hull Biofouling Prediction & Hull Performance Optimization")

st.write("""
This app predicts **biofouling severity** using logistic regression,
and provides **maintenance and safety recommendations**.
""")

# Inputs
vessel_speed = st.slider("Vessel Speed (kn)", 5, 25, 12)
idle_days = st.number_input("Idle Days", 0, 60, 10)
temp = st.slider("Sea Temperature (°C)", 20, 35, 28)
salinity = st.slider("Salinity (ppt)", 30, 40, 35)
days_since_clean = st.number_input("Days Since Last Cleaning", 0, 365, 60)
roughness = st.slider("Hull Roughness (mm)", 0.01, 0.2, 0.05)
friction = st.slider("Friction Coefficient", 0.001, 0.01, 0.002)
fuel_penalty = st.slider("Fuel Penalty (%)", 0, 30, 5)

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
fuel = fuel_consumption(power_kw)

st.subheader("📈 Hull Performance Metrics")
st.write(f"Resistance (N): {res:.2f}")
st.write(f"Power Required (kW): {power_kw:.2f}")
st.write(f"Speed after Fouling (kn): {speed_loss:.2f}")
st.write(f"Fuel Consumption (kg/hr): {fuel:.2f}")

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
fuel_values = [fuel_curve(vessel_speed, r) for r in fouling_range]

df_fuel = pd.DataFrame({
    "Hull Roughness (mm)": fouling_range,
    "Fuel Consumption (kg/hr)": fuel_values
})

fuel_chart = alt.Chart(df_fuel).mark_line().encode(
    x="Hull Roughness (mm)",
    y=alt.Y("Fuel Consumption (kg/hr)", scale=alt.Scale(domain=[0, 0.5]))
).properties(
    title="📊 Fuel Consumption vs Hull Fouling"
)

st.altair_chart(fuel_chart, use_container_width=True)
