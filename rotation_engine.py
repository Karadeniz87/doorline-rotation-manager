def run_rotation(employees, stations):

    available_employees = [
        e for e in employees
        if e.get("status") == "Verfügbar"
    ]

    employee_index = 0

    for station in stations:

        if not station["active"]:
            continue

        station["employee_1"] = None
        station["employee_2"] = None

        if employee_index < len(available_employees):
            employee = available_employees[employee_index]

            station["employee_1"] = (
                employee["firstname"] +
                " " +
                employee["lastname"]
            )

            employee_index += 1

    return {
        "assigned_employees": employee_index,
        "stations": stations
    }
