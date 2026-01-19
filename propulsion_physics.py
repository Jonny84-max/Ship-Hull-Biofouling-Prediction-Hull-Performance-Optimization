# Resistance due to hull fouling
def resistance_increase(roughness, vessel_speed):
    roughness: hull roughness (mm)
    vessel_speed: speed in knots
    return (1 + roughness * 15) * (vessel_speed ** 2)

# Power required
def power_required(resistance, vessel_speed):
    resistance: abstract resistance unit
    vessel_speed: knots
    speed_m_s = vessel_speed * 0.51444
    return resistance * speed_m_s  # Watts (scaled)

# Speed loss due to fouling
def speed_loss_due_to_fouling(roughness, vessel_speed):
    Simple empirical fouling speed-loss model
    loss_percent = roughness * 50
    loss_percent = min(loss_percent, 90)
    return vessel_speed * (1 - loss_percent / 100)

# Fuel consumption (L/hr)
def fuel_consumption_lph(power_kw, sfc=210, fuel_density=850):
    power_kw: engine power in kW
    sfc: specific fuel consumption (g/kWh)
    fuel_density: kg/m3 (Marine Diesel Oil)
    fuel_kg_per_hr = (power_kw * sfc) / 1000
    fuel_lph = (fuel_kg_per_hr / fuel_density) * 1000
    return fuel_lph

# Fuel consumption (tons/hr)
def fuel_consumption_tph(power_kw, sfc=210):
    fuel_kg_per_hr = (power_kw * sfc) / 1000
    return fuel_kg_per_hr / 1000

# Fuel curve vs fouling
def fuel_curve(vessel_speed, roughness):
    res = resistance_increase(roughness, vessel_speed)
    power_kw = power_required(res, vessel_speed) / 1000
    return fuel_consumption_lph(power_kw)
