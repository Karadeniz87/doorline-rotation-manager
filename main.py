from fastapi import FastAPI, HTTPException
from employee import Employee
from station import Station

app = FastAPI(
    title="Doorline Rotation Manager",
    version="1.0.0"
)

employees = []

DEFAULT_STATIONS = [
    "30L", "30R",
    "40L", "40R",
    "50L", "50R",
    "60L", "60R",
    "70L", "70R",
    "80L", "80R",
    "90L", "90R",
    "100L", "100R",
    "110L", "110R"
]

stations = []

for station_name in DEFAULT_STATIONS:
    stations.append({
        "name": station_name,
        "active": True,
        "double_takt": station_name in [
            "40L", "40R",
            "50L", "50R",
            "60L", "60R",
            "70L", "70R"
        ],
        "assigned_employee": None,
        "support_required": False
    })


# =====================================
# SYSTEM
# =====================================

@app.get("/")
def home():
    return {
        "app": "Doorline Rotation Manager",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =====================================
# EMPLOYEES
# =====================================

@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employees[employee_id]


@app.post("/employees")
def add_employee(employee: Employee):
    employee_data = employee.model_dump()

    employees.append(employee_data)

    return {
        "message": "Mitarbeiter hinzugefügt",
        "employee_id": len(employees) - 1,
        "employee": employee_data
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee.model_dump()

    return {
        "message": "Mitarbeiter aktualisiert",
        "employee": employees[employee_id]
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted_employee
    }


# =====================================
# STATIONS
# =====================================

@app.get("/stations")
def get_stations():
    return stations


@app.put("/stations/{station_name}/activate")
def activate_station(station_name: str):
    for station in stations:
        if station["name"] == station_name:
            station["active"] = True
            return station

    raise HTTPException(
        status_code=404,
        detail="Station nicht gefunden"
    )


@app.put("/stations/{station_name}/deactivate")
def deactivate_station(station_name: str):
    for station in stations:
        if station["name"] == station_name:
            station["active"] = False
            return station

    raise HTTPException(
        status_code=404,
        detail="Station nicht gefunden"
    )


# =====================================
# ROTATION ENGINE
# =====================================

@app.post("/rotation/run")
def run_rotation():

    available_employees = [
        e for e in employees
        if e["status"] == "Verfügbar"
    ]

    # Reset
    for station in stations:
        station["assigned_employee"] = None
        station["support_required"] = False

    support_needed = 0

    for station in stations:

        if not station["active"]:
            continue

        skill_name = f"skill_{station['name']}"

        candidates = [
            employee for employee in available_employees
            if employee.get(skill_name, False)
        ]

        if len(candidates) > 0:
            selected_employee = min(
                candidates,
                key=lambda x: x.get("fairness_points", 0)
            )

            station["assigned_employee"] = (
                f"{selected_employee['firstname']} "
                f"{selected_employee['lastname']}"
            )

            selected_employee["fairness_points"] += 1
            available_employees.remove(selected_employee)

        else:
            station["support_required"] = True
            support_needed += 1

    return {
        "stations": stations,
        "support_needed": support_needed
    }


# =====================================
# KPI
# =====================================

@app.get("/stats")
def stats():

    return {
        "employees_total": len(employees),
        "available": len([
            e for e in employees
            if e["status"] == "Verfügbar"
        ]),
        "urlaub": len([
            e for e in employees
            if e["status"] == "Urlaub"
        ]),
        "krank": len([
            e for e in employees
            if e["status"] == "Krank"
        ]),
        "support": len([
            s for s in stations
            if s["support_required"]
        ]),
        "active_stations": len([
            s for s in stations
            if s["active"]
        ])
    }
@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employees[employee_id]


@app.post("/employees")
def add_employee(employee: Employee):
    employee_data = employee.model_dump()
    employees.append(employee_data)

    return {
        "message": "Mitarbeiter hinzugefügt",
        "employee_id": len(employees) - 1,
        "employee": employee_data
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee.model_dump()

    return {
        "message": "Mitarbeiter aktualisiert",
        "employee": employees[employee_id]
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted_employee
    }


# =====================
# STATIONS
# =====================

@app.get("/stations")
def get_stations():
    return stations


@app.get("/stations/{station_id}")
def get_station(station_id: int):
    if station_id >= len(stations):
        raise HTTPException(
            status_code=404,
            detail="Station nicht gefunden"
        )

    return stations[station_id]


@app.post("/stations")
def add_station(station: Station):
    station_data = station.model_dump()
    stations.append(station_data)

    return {
        "message": "Station hinzugefügt",
        "station_id": len(stations) - 1,
        "station": station_data
    }


@app.put("/stations/{station_id}")
def update_station(station_id: int, station: Station):
    if station_id >= len(stations):
        raise HTTPException(
            status_code=404,
            detail="Station nicht gefunden"
        )

    stations[station_id] = station.model_dump()

    return {
        "message": "Station aktualisiert",
        "station": stations[station_id]
    }


@app.delete("/stations/{station_id}")
def delete_station(station_id: int):
    if station_id >= len(stations):
        raise HTTPException(
            status_code=404,
            detail="Station nicht gefunden"
        )

    deleted_station = stations.pop(station_id)

    return {
        "message": "Station gelöscht",
        "station": deleted_station
    }


# =====================
# KPI
# =====================

@app.get("/stats")
def stats():
    return {
        "employees_total": len(employees),
        "stations_total": len(stations),
        "available": len(
            [e for e in employees if e.get("status") == "Verfügbar"]
        ),
        "urlaub": len(
            [e for e in employees if e.get("status") == "Urlaub"]
        ),
        "krank": len(
            [e for e in employees if e.get("status") == "Krank"]
        ),
        "support": len(
            [e for e in employees if e.get("status") == "Support"]
        )
    }
