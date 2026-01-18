"""
Rule-based operational safety checks
"""

def check_operational_safety(speed_kn, hull_roughness, days_since_cleaning):
    if hull_roughness > 0.08:
        return "UNSAFE: Excessive hull roughness"

    if speed_kn > 18 and hull_roughness > 0.06:
        return "WARNING: High speed with fouled hull"

    if days_since_cleaning > 365:
        return "WARNING: Hull cleaning overdue"

    return "SAFE: Operating within limits"
