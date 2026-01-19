def resistance_increase(roughness, vessel_speed):
    # Simple resistance formula (example)
    return (1 + roughness * 10) * ( vessel_speed ** 2)

def power_required(resistance, vessel_speed):    
    speed_m_s = vessel_speed * 0.51444
    return resistance * speed_m_s

def speed_loss_due_to_fouling(roughness, vessel_speed):
    loss_percent = roughness * 50
    # Prevent negative speed
    if loss_percent >= 100:
        loss_percent = 99
    return vessel_speed * (1 - loss_percent / 100)

def fuel_consumption(power_kw):
    # Simple fuel burn model (example)
    return power_kw * 0.2

def fuel_curve(vessel_speed, roughness):
    res = resistance_increase(roughness, speed_kn)
    power_kw = power_required(res, vessel_speed) / 1000
    return fuel_consumption(power_kw)
