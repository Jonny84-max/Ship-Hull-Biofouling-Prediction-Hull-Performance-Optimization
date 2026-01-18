import streamlit as st
import pandas as pd
import joblib
import numpy as np
import altair as alt
from pathlib import Path

# Import your helper modules (wrap import in try/except to give a helpful error)
try:
    from propulsion_physics import (
        fuel_curve,
        resistance_increase,
        power_required,
        speed_loss_due_to_fouling,
        fuel_consumption,
    )
    from safety_rules import check_operational_safety
    from maintenance_schedule import maintenance_action
except Exception as e:
    st.error(f"Failed to import helper modules: {e}")
    st.stop()

# -----------------------------
# Cached model loader
# -----------------------------
@st.cache_resource
def load_model(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Model file not found at {path}")
    return joblib.load(path)

try:
    model = load_model("biofouling_model.pkl")
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()

# -----------------------------
# Page config + title
# -----------------------------
st.set_page_config(
    page_title="Ship Hull Biofouling Prediction & Hull Performance Optimization",
    layout="wide",
)

st.title("🚢 Ship Hull Biofouling Prediction & Hull Performance Optimization")
st.write(
    "This app predicts biofouling severity and provides maintenance & safety recommendations."
)

# -----------------------------
# Inputs (use sidebar for controls)
# -----------------------------
with st.sidebar:
    st.header("Input Parameters")
    speed = st.slider("Vessel Speed (kn)", min_value=5.0, max_value=25.0, value=12.0, step=0.5)
    idle_days = st.number_input("Idle Days", min_value=0, max_value=365, value=10)
    temp = st.slider("Sea Temperature (°C)", min_value=0.0, max_value=40.0, value=28.0, step=0.5)
    salinity = st.slider("Salinity (ppt)", min_value=0.0, max_value=40.0, value=35.0, step=0.1)
    days_since_clean = st.number_input("Days Since Last Cleaning", min_value=0, max_value=3650, value=60)
    roughness = st.slider("Hull Roughness (mm)", min_value=0.001, max_value=1.0, value=0.05, step=0.001)
    friction = st.slider("Friction Coefficient", min_value=0.0001, max_value=0.05, value=0.002, step=0.0001)
    fuel_penalty = st.slider("Fuel Penalty (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

# -----------------------------
# Validate / prepare input data
# -----------------------------
input_data = pd.DataFrame(
    {
        "sea_temperature": [float(temp)],
        "salinity": [float(salinity)],
        "idle_days": [int(idle_days)],
        "avg_speed": [float(speed)],
        "days_since_cleaning": [int(days_since_clean)],
        "hull_roughness": [float(roughness)],
        "friction_coeff": [float(friction)],
        "fuel_penalty": [float(fuel_penalty)],
    }
)

st.subheader("📌 Input Summary")
st.write(input_data.T.rename(columns={0: "value"}))

# -----------------------------
# Prediction (class + probability)
# -----------------------------
try:
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_data)[0]
        pred_class = model.predict(input_data)[0]
        # Attempt to get class labels (if provided as attribute)
        try:
            classes = model.classes_
        except Exception:
            classes = ["0", "1"]
        # Build readable probability display
        proba_display = {str(c): f"{p*100:.1f}%" for c, p in zip(classes, proba)}
        st.subheader("📌 Prediction Result")
        st.write(f"**Biofouling Severity (predicted):** {pred_class}")
        st.write("**Prediction probabilities:**")
        st.write(proba_display)
    else:
        pred_class = model.predict(input_data)[0]
        st.subheader("📌 Prediction Result")
        st.write(f"**Biofouling Severity (predicted):** {pred_class}")
except Exception as e:
    st.error(f"Prediction failed: {e}")
    st.stop()

# -----------------------------
# Safety + Maintenance
# -----------------------------
st.subheader("🛟 Safety & Maintenance Recommendations")
try:
    safety_msg = check_operational_safety(speed, roughness, days_since_clean)
    maintenance_msg = maintenance_action(pred_class)
    st.write(safety_msg)
    st.write(maintenance_msg)
except Exception as e:
    st.warning(f"Could not compute safety/maintenance recommendations: {e}")

# -----------------------------
# Physics Metrics
# -----------------------------
st.subheader("📈 Hull Performance Metrics")
try:
    res = resistance_increase(roughness, speed)
    power_kw = power_required(res, speed) / 1000.0
    fouled_speed = speed_loss_due_to_fouling(roughness, speed)
    fuel = fuel_consumption(power_kw)  # ensure function expects kW
    st.metric("Resistance (N)", f"{res:.2f}")
    st.metric("Power Required (kW)", f"{power_kw:.2f}")
    st.metric("Speed after Fouling (kn)", f"{fouled_speed:.2f}")
    st.metric("Fuel Consumption (kg/hr)", f"{fuel:.2f}")
except Exception as e:
    st.warning(f"Could not compute physical metrics: {e}")

# -----------------------------
# Charts (Altair)
# -----------------------------
st.subheader("📊 Fuel Consumption vs Fouling")
fouling_range = np.linspace(max(0.001, roughness * 0.2), max(0.2, roughness * 3), 50)
# Ensure functions are vector-safe; else use list comprehension
try:
    fuel_values = [fuel_curve(speed, r) for r in fouling_range]
    fuel_df = pd.DataFrame({"Roughness (mm)": fouling_range, "Fuel Consumption (kg/hr)": fuel_values})
    chart1 = (
        alt.Chart(fuel_df)
        .mark_line()
        .encode(x=alt.X("Roughness (mm)", scale=alt.Scale(zero=False)), y=alt.Y("Fuel Consumption (kg/hr)"))
        .properties(title="Fuel Consumption vs Hull Fouling")
    )
    st.altair_chart(chart1, use_container_width=True)
except Exception as e:
    st.warning(f"Could not render fuel chart: {e}")

st.subheader("📉 Speed Loss vs Fouling")
try:
    speed_values = [speed_loss_due_to_fouling(r, speed) for r in fouling_range]
    speed_df = pd.DataFrame({"Roughness (mm)": fouling_range, "Speed (kn)": speed_values})
    chart2 = (
        alt.Chart(speed_df)
        .mark_line()
        .encode(x=alt.X("Roughness (mm)", scale=alt.Scale(zero=False)), y=alt.Y("Speed (kn)"))
        .properties(title="Speed Loss vs Hull Fouling")
    )
    st.altair_chart(chart2, use_container_width=True)
except Exception as e:
    st.warning(f"Could not render speed chart: {e}")

# -----------------------------
# Footer / Notes
# -----------------------------
st.write("---")
st.caption("Model: logistic regression (joblib). Ensure biofouling_model.pkl and helper modules are present.")
