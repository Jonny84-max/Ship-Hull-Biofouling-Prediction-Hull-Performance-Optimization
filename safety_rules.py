def check_operational_safety(speed_kn, roughness, days_since_cleaning):
    warnings = []

    # Rule 1: Speed limit
    if speed_kn > 22:
        warnings.append("WARNING: Speed too high for safety. Reduce speed.")

    # Rule 2: Roughness limit
    if roughness > 0.15:
        warnings.append("WARNING: Hull roughness is too high. Immediate cleaning recommended.")

    # Rule 3: Cleaning limit
    if days_since_cleaning > 120:
        warnings.append("WARNING: Hull overdue for cleaning. Schedule maintenance.")

    if len(warnings) == 0:
        return "SAFE: Operating within limits."
    else:
        return " ".join(warnings)
