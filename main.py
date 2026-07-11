from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from employee import Employee

# SQLite Vorbereitung
try:
    from database import Base, engine
    import models

    Base.metadata.create_all(bind=engine)
except Exception:
    pass


app = FastAPI(
    title="Doorline Rotation Manager",
    version="4.0.0"
)

# Frontend
app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

# Stationen
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

# Doppeltakt
double_takt_stations = {
    "40L", "40R",
    "50L", "50R",
    "60L", "60R",
    "70L", "70R"
}

# Mitarbeiter
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
    Employee(firstname="Rawad", lastname="Al Akle")
]


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {
        "status": "running"
    }


# ---------------- EMPLOYEES ----------------

@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employees[employee_id]


@app.post("/employees")
def add_employee(employee: Employee):
    employees.append(employee)
    return employee


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):

    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee
    return employee


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    deleted = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted
    }


# ---------------- STATIONS ----------------

@app.get("/stations")
def get_stations():

    return [
        {
            "name": station,
            "double_takt_allowed": station in double_takt_stations
        }
        for station in stations
    ]


# ---------------- ROTATION ----------------

@app.post("/rotation/run")
def run_rotation():

    rotation_result = []
    assigned_employees = set()
    support_employees = []

    # Stations zurücksetzen
    for employee in employees:
        employee.station = None

    # Faire Verteilung
    sorted_employees = sorted(
        employees,
        key=lambda x: x.fairness_points
    )

    for station in stations:

        assigned_employee = None
        skill_name = f"skill_{station}"

        for employee in sorted_employees:

            if employee.is_sick:
                continue

            if employee.is_vacation:
                continue

            if employee.lastname in assigned_employees:
                continue

            if employee.last_station == station:
                continue

            if not getattr(employee, skill_name, False):
                continue

            assigned_employee = (
                f"{employee.firstname} "
                f"{employee.lastname}"
            )

            employee.last_station = employee.station
            employee.station = station
            employee.fairness_points += 1

            assigned_employees.add(
                employee.lastname
            )

            break

        rotation_result.append({
            "name": station,
            "employee_1": assigned_employee,
            "employee_2": None,
            "support_required": assigned_employee is None,
            "double_takt_allowed": station in double_takt_stations
        })

    # Support Mitarbeiter
    for employee in employees:

        if employee.is_sick:
            continue

        if employee.is_vacation:
            continue

        if employee.lastname not in assigned_employees:

            employee.station = "Support"

            support_employees.append(
                f"{employee.firstname} "
                f"{employee.lastname}"
            )

    return {
        "message": "Rotation durchgeführt",
        "stations": rotation_result,
        "support_employees": support_employees
    }


# ---------------- KPI ----------------

@app.get("/stats")
def stats():

    sick = sum(
        1 for e in employees
        if e.is_sick
    )

    vacation = sum(
        1 for e in employees
        if e.is_vacation
    )

    support = sum(
        1 for e in employees
        if e.station == "Support"
    )

    available = len(employees) - sick - vacation

    return {
        "employees_total": len(employees),
        "available": available,
        "vacation": vacation,
        "sick": sick,
        "support": support,
        "double_takt": len(double_takt_stations)
    }


@app.get("/fairness")
def fairness():

    return {
        f"{e.firstname} {e.lastname}":
        e.fairness_points
        for e in employees
    }


@app.get("/flexibility")
def flexibility():

    return {
        "double_takt_stations": list(
            double_takt_stations
        )
    }    Employee(firstname="Oliwia", lastname="Budkowska"),
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
    Employee(firstname="Rawad", lastname="Al Akle")
]


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {
        "status": "running"
    }


# ---------------- EMPLOYEES ----------------

@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employees[employee_id]


@app.post("/employees")
def add_employee(employee: Employee):
    employees.append(employee)
    return employee


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):

    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee
    return employee


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    if employee_id < 0 or employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employees.pop(employee_id)


# ---------------- STATIONS ----------------

@app.get("/stations")
def get_stations():

    return [
        {
            "name": station,
            "double_takt_allowed": station.startswith(
                ("40", "50", "60", "70")
            )
        }
        for station in stations
    ]


# ---------------- ROTATION ----------------

@app.post("/rotation/run")
def run_rotation():

    rotation_result = []
    assigned_employees = set()
    support_employees = []

    # Wenigste Fairness zuerst
    sorted_employees = sorted(
        employees,
        key=lambda x: x.fairness_points
    )

    for station in stations:

        assigned_employee = None
        skill_name = f"skill_{station}"

        for employee in sorted_employees:

            # Krank
            if employee.is_sick:
                continue

            # Urlaub
            if employee.is_vacation:
                continue

            # Bereits eingeplant
            if employee.lastname in assigned_employees:
                continue

            # Nicht direkt wieder gleiche Station
            if employee.last_station == station:
                continue

            # Skill vorhanden
            if not getattr(employee, skill_name, False):
                continue

            assigned_employee = (
                f"{employee.firstname} "
                f"{employee.lastname}"
            )

            employee.last_station = employee.station
            employee.station = station
            employee.fairness_points += 1

            assigned_employees.add(
                employee.lastname
            )

            break

        rotation_result.append({
            "name": station,
            "employee_1": assigned_employee,
            "employee_2": None,
            "support_required": assigned_employee is None,
            "double_takt_allowed": station.startswith(
                ("40", "50", "60", "70")
            )
        })

    # Support Mitarbeiter
    for employee in employees:

        if employee.is_sick:
            continue

        if employee.is_vacation:
            continue

        if employee.lastname not in assigned_employees:

            employee.station = "Support"

            support_employees.append(
                f"{employee.firstname} "
                f"{employee.lastname}"
            )

    return {
        "message": "Rotation durchgeführt",
        "stations": rotation_result,
        "support_employees": support_employees
    }


# ---------------- KPI ----------------

@app.get("/stats")
def stats():

    sick = sum(
        1 for e in employees
        if e.is_sick
    )

    vacation = sum(
        1 for e in employees
        if e.is_vacation
    )

    support = sum(
        1 for e in employees
        if e.station == "Support"
    )

    available = len(employees) - sick - vacation

    return {
        "employees_total": len(employees),
        "available": available,
        "vacation": vacation,
        "sick": sick,
        "support": support,
        "double_takt": 0
    }


@app.get("/fairness")
def fairness():

    return {
        f"{e.firstname} {e.lastname}":
        e.fairness_points
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
