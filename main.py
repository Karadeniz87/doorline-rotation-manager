from fastapi import FastAPI, HTTPException
from employee import Employee
from station import Station

app = FastAPI(
    title="Doorline Rotation Manager",
    version="1.0.0"
)

# Speicher
employees = []
stations = []

# =====================================
# HOME
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


# =====================================
# KPI
# =====================================

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
