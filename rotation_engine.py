def run_rotation(employees, stations):

    available = [
        employee for employee in employees
        if employee["status"] == "Verfügbar"
    ]

    assigned = []

    for station in stations:

        station_name = station["name"]

        station["employee_1"] = None
        station["employee_2"] = None

        for employee in available:

            skill_name = f"skill_{station_name}"

            if (
                employee.get(skill_name, False)
                and employee["lastname"] not in assigned
            ):

                station["employee_1"] = (
                    employee["firstname"]
                    + " "
                    + employee["lastname"]
                )

                assigned.append(
                    employee["lastname"]
                )

                break

    return {
        "assigned": len(assigned),
        "stations": stations
    }
