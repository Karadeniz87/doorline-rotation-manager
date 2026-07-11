from fastapi import FastAPI, HTTPException
from employee import Employee
from rotation_engine import run_rotation

app = FastAPI(
    title="Doorline Rotation Manager",
    version="2.0.0"
)

employees = []

stations = []

station_names = [
    "30L","30R",
    "40L","40R",
    "50L","50R",
    "60L","60R",
    "70L","70R",
    "80L","80R",
    "90L","90R",
    "100L","100R",
    "110L","110R"
]

for station in station_names:
    stations.append({
        "name": station,
        "active": True,
        "double_takt_allowed": station in [
            "40L","40R",
            "50L","50R",
            "60L","60R",
            "70L","70R"
        ],
        "double_takt_active": False,
        "employee_1": None,
        "employee_2": None,
        "support_required": False
    })

default_employees = [
    ("Waldemar","Krupowicz"),
    ("Christian","Francke"),
    ("Cagliyan","Aslandag"),
    ("Mhd Nour","Fallah"),
    ("Oliwia","Budkowska"),
    ("Maxwell Kofi","Mensah"),
    ("Adolphe Boumsong","Dimouk"),
    ("Fabian","Dubaj"),
    ("Salh","Alamash"),
    ("Sarah Akuma","Ukpo"),
    ("Germay","Mehari"),
    ("Karolina","Włodarczyk"),
    ("Md Jowel","Hossain"),
    ("Renata","Molek"),
    ("Thaer","Al Gharib"),
    ("Kwame","Opoku"),
    ("Rawad","Al Akle")
]

for first, last in default_employees:
    employees.append({
        "firstname": first,
        "lastname": last,
        "status": "Verfügbar",
        "fairness_points": 0
    })

@app.get("/")
def home():
    return {
        "app": "Doorline Rotation Manager",
        "employees": len(employees),
        "stations": len(stations)
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

@app.get("/stations")
def get_stations():
    return stations

@app.post("/rotation/run")
def rotation():
    return run_rotation(
        employees,
        stations
    )

@app.get("/stats")
def stats():
    return {
        "employees": len(employees),
        "stations": len(stations),
        "available": len([
            e for e in employees
            if e["status"] == "Verfügbar"
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
