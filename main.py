from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from employee import Employee

app = FastAPI(
    title="Doorline Rotation Manager",
    version="1.0.0"
)

# Frontend bereitstellen
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Mitarbeiterliste
employees = [
    Employee(firstname="Waldemar", lastname="Krupowicz"),
    Employee(firstname="Christian", lastname="Francke"),
    Employee(firstname="Cagliyan", lastname="Aslandag"),
    Employee(firstname="Mhd Nour", lastname="Fallah"),
    Employee(firstname="Oliwia", lastname="Budkowska"),
    Employee(firstname="Maxwell Kofi", lastname="Mensah"),
    Employee(firstname="Adolphe Boumsong", lastname="Dimouk"),
    Employee(firstname="Fabian", lastname="Dubaj"),
    Employee(firstname="Salh", lastname="Alamash"),
    Employee(firstname="Sarah Akuma", lastname="Ukpo"),
    Employee(firstname="Germay", lastname="Mehari"),
    Employee(firstname="Karolina", lastname="Włodarczyk"),
    Employee(firstname="Md Jowel", lastname="Hossain"),
    Employee(firstname="Renata", lastname="Molek"),
    Employee(firstname="Thaer", lastname="Al Gharib"),
    Employee(firstname="Kwame", lastname="Opoku"),
    Employee(firstname="Rawad", lastname="Al Akle"),
]

stations = [
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


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {"status": "running"}


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
    employees.append(employee)

    return {
        "message": "Mitarbeiter hinzugefügt",
        "employee": employee
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee
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


@app.get("/stations")
def get_stations():
    result = []

    for station in stations:
        result.append({
            "name": station,
            "active": True,
            "employee_1": None,
            "employee_2": None,
            "double_takt_allowed": station.startswith(
                ("40", "50", "60", "70")
            )
        })

    return result


@app.post("/rotation/run")
def run_rotation():

    result = []
    assigned_employees = set()

    for station in stations:

        assigned_employee = None

        skill_name = f"skill_{station}"

        for employee in employees:

            # Nur verfügbare Mitarbeiter
            if employee.status != "Verfügbar":
                continue

            # Mitarbeiter nicht doppelt einsetzen
            if employee.lastname in assigned_employees:
                continue

            # Prüfen ob Mitarbeiter die Station beherrscht
            if getattr(employee, skill_name, False):

                assigned_employee = (
                    f"{employee.firstname} "
                    f"{employee.lastname}"
                )

                assigned_employees.add(
                    employee.lastname
                )

                break

        result.append({
            "name": station,
            "active": True,
            "employee_1": assigned_employee,
            "employee_2": None,
            "support_required": False,
            "double_takt_allowed": station.startswith(
                ("40", "50", "60", "70")
            )
        })

    return {
        "message": "Rotation durchgeführt",
        "stations": result
    }
    result = []

    employee_index = 0

    for station in stations:
        assigned_employee = None

        if employee_index < len(employees):
            assigned_employee = (
                f"{employees[employee_index].firstname} "
                f"{employees[employee_index].lastname}"
            )
            employee_index += 1

        result.append({
            "name": station,
            "active": True,
            "employee_1": assigned_employee,
            "employee_2": None,
            "support_required": False
        })

    return {
        "message": "Rotation durchgeführt",
        "stations": result
    }


@app.get("/stats")
def stats():
    return {
        "employees_total": len(employees),
        "available": len(employees),
        "vacation": 0,
        "sick": 0,
        "support": 0,
        "double_takt": 0
    }


@app.get("/fairness")
def fairness():
    return {
        f"{e.firstname} {e.lastname}": e.fairness_points
        for e in employees
    }


@app.get("/flexibility")
def flexibility():
    return {
        "double_takt_stations": [
            "40L", "40R",
            "50L", "50R",
            "60L", "60R",
            "70L", "70R"
        ]
    }
