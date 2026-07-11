rotation_history = []


def save_rotation(station, employee):
    rotation_history.append({
        "station": station,
        "employee": employee
    })


def get_history():
    return rotation_history
