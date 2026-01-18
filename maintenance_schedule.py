def maintenance_action(prediction):
    if prediction == 0:
        return "Maintenance Action: No immediate action needed. Continue monitoring."
    elif prediction == 1:
        return "Maintenance Action: Plan hull cleaning soon. Reduce idle time."
    elif prediction == 2:
        return "Maintenance Action: Immediate hull cleaning required! Check antifouling paint and inspect hull."
    else:
        return "Maintenance Action: Unknown severity."
