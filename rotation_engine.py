DOUBLE_TAKT_STATIONS = {
    "40L", "40R",
    "50L", "50R",
    "60L", "60R",
    "70L", "70R"
}


def run_rotation(employees, stations):
    return {
        "message": "Rotation Engine bereit",
        "employees": len(employees),
        "stations": len(stations)
    }
