"""
Maintenance decision rules based on fouling severity
"""

def maintenance_action(fouling_class):
    if fouling_class == 0:
        return "No maintenance required"
    elif fouling_class == 1:
        return "Schedule inspection and partial cleaning"
    elif fouling_class == 2:
        return "Immediate hull cleaning recommended"
    else:
        return "Invalid fouling class"
