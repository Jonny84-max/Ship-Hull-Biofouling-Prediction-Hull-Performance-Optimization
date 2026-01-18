def resistance_increase(roughness, speed_kn):
    # Simple resistance formula (example)
    return (1 + roughness * 10) * (speed_kn ** 2)

def power_required(resistance, speed_kn):    
    speed_m_s = speed_kn * 0.51444
    return resistance * speed_m_s

def speed_loss_due_to_fouling(roughness, speed_kn):
    # Speed loss increases with roughness
    loss_percent = roughness * 50
    return speed_kn * (1 - loss_percent / 100)

def fuel_consumption(power_kw):
    # Simple fuel burn model (example)
    return power_kw * 0.2

def fuel_curve(speed_kn, roughness):
    res = resistance_increase(roughness, speed_kn)
    power_kw = power_required(res, speed_kn) / 1000
    return fuel_consumption(power_kw)
