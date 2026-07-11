from fastapi import FastAPI, HTTPException
from employee import Employee
from station import Station
from rotation_engine import run_rotation

app = FastAPI(
    title="Doorline Rotation Manager",
    version="1.0.0"
)

# =========================
# Mitarbeiter Datenbank
# =========================

employees = [
    {
        "firstname": "Waldemar",
        "lastname": "Krupowicz",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Christian",
        "lastname": "Francke",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Cagliyan",
        "lastname": "Aslandag",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Mhd Nour",
        "lastname": "Fallah",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Oliwia",
        "lastname": "Budkowska",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Maxwell Kofi",
        "lastname": "Mensah",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Adolphe Boumsong",
        "lastname": "Dimouk",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Fabian",
        "lastname": "Dubaj",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Salh",
        "lastname": "Alamash",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Sarah Akuma",
        "lastname": "Ukpo",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Germay",
        "lastname": "Mehari",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Karolina",
        "lastname": "Włodarczyk",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Md Jowel",
        "lastname": "Hossain",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Renata",
        "lastname": "Molek",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Thaer",
        "lastname": "Al Gharib",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Kwame",
        "lastname": "Opoku",
        "status": "Verfügbar",
        "fairness_points": 0
    },
    {
        "firstname": "Rawad",
        "lastname": "Al Akle",
        "status": "Verfügbar",
        "fairness_points": 0
    }
]

# =========================
# Stationen
# =========================

stations = []

for station_name in [
    "30L", "30R",
    "40L", "40R",
    "50L", "50R",
    "60L", "60R",
    "70L", "70R",
    "80L", "80R",
    "90L", "90R",
    "100L", "100R",
    "110L", "110R"
]:
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

# =========================
# System
# =========================

@app.get("/")
def home():
    return {
        "app": "Doorline Rotation Manager",
        "version": "1.0.0",
        "employees": len(employees),
        "stations": len(stations),
        "status": "running"
    }

# =========================
# Mitarbeiter
# =========================

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
        "employee": employee_data
    }


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: Employee
):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee.model_dump()

    return employees[employee_id]


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    deleted = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted
    }

# =========================
# Stationen
# =========================

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

# =========================
# Rotation
# =========================

@app.post("/rotation/run")
def start_rotation():
    return run_rotation(
        employees,
        stations
    )

# =========================
# KPI
# =========================

@app.get("/stats")
def stats():
    return {
        "employees_total": len(employees),
        "stations_total": len(stations),
        "available": len(
            [e for e in employees
             if e["status"] == "Verfügbar"]
        ),
        "urlaub": len(
            [e for e in employees
             if e["status"] == "Urlaub"]
        ),
        "krank": len(
            [e for e in employees
             if e["status"] == "Krank"]
        )
    }
