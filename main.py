from fastapi import FastAPI, HTTPException
from employee import Employee
from rotation_engine import run_rotation

app = FastAPI(
    title="Doorline Rotation Manager",
    version="1.0.0"
)

# =========================
# Mitarbeiter
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

station_names = [
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

double_takt_stations = [
    "40L", "40R",
    "50L", "50R",
    "60L", "60R",
    "70L", "70R"
]

for station in station_names:
    stations.append({
        "name": station,
        "active": True,
        "double_takt_allowed": station in double_takt_stations,
        "double_takt_active": False,
        "employee_1": None,
        "employee_2": None,
        "support_required": False
    })

# =========================
# System
# =========================

@app.get("/")
def home():
    return {
        "app": "Doorline Rotation Manager",
        "status": "running",
        "employees": len(employees),
        "stations": len(stations)
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
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
    employees.append(employee.model_dump())
    return employee


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

    return employees.pop(employee_id)

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

        "available": len([
            e for e in employees
            if e.get("status") == "Verfügbar"
        ]),

        "urlaub": len([
            e for e in employees
            if e.get("status") == "Urlaub"
        ]),

        "krank": len([
            e for e in employees
            if e.get("status") == "Krank"
        ]),

        "support": len([
            s for s in stations
            if s.get("support_required")
        ]),

        "double_takt": len([
            s for s in stations
            if s.get("double_takt_active")
        ])
    }


@app.get("/fairness")
def fairness():
    return sorted(
        employees,
        key=lambda x: x.get(
            "fairness_points",
            0
        )
    )


@app.get("/flexibility")
def flexibility():

    result = []

    for employee in employees:

        skills = len([
            key for key, value in employee.items()
            if key.startswith("skill_") and value
        ])

        result.append({
            "employee":
                f"{employee['firstname']} "
                f"{employee['lastname']}",
            "skills": skills
        })

    result.sort(
        key=lambda x: x["skills"],
        reverse=True
    )

    return result
