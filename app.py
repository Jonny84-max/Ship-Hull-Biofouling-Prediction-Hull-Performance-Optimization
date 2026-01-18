import streamlit as st
import pandas as pd
import joblib
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# Import your helper modules
from propulsion_physics import (
    fuel_curve,
    resistance_increase,
    power_required,
    speed_loss_due_to_fouling,
    fuel_consumption
)

from safety_rules import check_operational_safety
from maintenance_schedule import maintenance_action

# -----------------------------
# Load the model
# -----------------------------
model = joblib.load("biofouling_model.pkl")

# -----------------------------
# App Title
# -----------------------------
st.title("🚢 Ship Hull Biofouling Prediction & Hull Performance Optimization")

st.write("""
This app predicts **biofouling severity** using logistic regression,
and provides **maintenance and safety recommendations**.
""")

# -----------------------------
# Inputs
# -----------------------------
speed = st.slider("Vessel Speed (kn)", 5, 25, 12)
idle_days = st.number_input("Idle Days", 0, 60, 10)
temp = st.slider("Sea Temperature (°C)", 20, 35, 28)
salinity = st.slider("Salinity (ppt)", 30, 40, 35)
days_since_clean = st.number_input("Days Since Last Cleaning", 0, 365, 60)
roughness = st.slider("Hull Roughness (mm)", 0.01, 0.2, 0.05)
friction = st.slider("Friction Coefficient", 0.001, 0.01, 0.002)
fuel_penalty = st.slider("Fuel Penalty (%)", 0, 30, 5)

# -----------------------------
# Prediction
# -----------------------------
input_data = pd.DataFrame({
    "sea_temperature": [temp],
    "salinity": [salinity],
    "idle_days": [idle_days],
    "avg_speed": [speed],
    "days_since_cleaning": [days_since_clean],
    "hull_roughness": [roughness],
    "friction_coeff": [friction],
    "fuel_penalty": [fuel_penalty]
})

prediction = model.predict(input_data)[0]

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

# -----------------------------
# Safety + Maintenance
# -----------------------------
safety_message = check_operational_safety(speed, roughness, days_since_clean)
st.write(safety_message)

maintenance_message = maintenance_action(prediction)
st.write(maintenance_message)

# -----------------------------
# Performance Metrics
# -----------------------------
res = resistance_increase(roughness, speed)
power_kw = power_required(res, speed) / 1000
speed_loss = speed_loss_due_to_fouling(roughness, speed)
fuel = fuel_consumption(power_kw)

st.subheader("📈 Hull Performance Metrics")
st.write(f"Resistance (N): {res:.2f}")
st.write(f"Power Required (kW): {power_kw:.2f}")
st.write(f"Speed after Fouling (kn): {speed_loss:.2f}")
st.write(f"Fuel Consumption (kg/hr): {fuel:.2f}")

st.subheader("📊 Fuel Consumption vs Hull Fouling")

roughness_range = np.linspace(0.01, 0.2, 30)

fuel_values = [
    fuel_curve(vessel_speed, r) for r in roughness_range
]

plot_df = pd.DataFrame({
    "Hull Roughness (mm)": roughness_range,
    "Fuel Consumption (kg/hr)": fuel_values
})

chart = alt.Chart(plot_df).mark_line(point=True).encode(
    x="Hull Roughness (mm)",
    y="Fuel Consumption (kg/hr)"
)

st.altair_chart(chart, use_container_width=True)

st.subheader("📉 Speed Loss vs Hull Fouling")

speed_values = [
    speed_loss_due_to_fouling(r, vessel_speed)
    for r in roughness_range
]

speed_df = pd.DataFrame({
    "Hull Roughness (mm)": roughness_range,
    "Effective Speed (kn)": speed_values
})

speed_chart = alt.Chart(speed_df).mark_line(color="red").encode(
    x="Hull Roughness (mm)",
    y="Effective Speed (kn)"
)

st.altair_chart(speed_chart, use_container_width=True)

# -----------------------------
# Charts (Altair)
# -----------------------------
st.subheader("📊 Fuel Consumption vs Hull Fouling")

fouling_range = np.linspace(0.01, 0.2, 50)
fuel_values = [fuel_curve(speed, r) for r in fouling_range]

df_fuel = pd.DataFrame({
    "Hull Roughness (mm)": fouling_range,
    "Fuel Consumption (kg/hr)": fuel_values,  # use the list you computed above
})
