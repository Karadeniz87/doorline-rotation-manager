from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import EmployeeDB, RotationHistory
from employee import Employee

Base.metadata.create_all(bind=engine)

# ----------------------------------------------------
# Mitarbeiter automatisch anlegen
# ----------------------------------------------------

db_seed = SessionLocal()

if db_seed.query(EmployeeDB).count() == 0:

    employees_seed = [
        EmployeeDB(firstname="Waldemar", lastname="Krupowicz"),
        EmployeeDB(firstname="Christian", lastname="Francke"),
        EmployeeDB(firstname="Cagliyan", lastname="Aslandag"),
        EmployeeDB(firstname="Mhd Nour", lastname="Fallah"),
        EmployeeDB(firstname="Oliwia", lastname="Budkowska"),
        EmployeeDB(firstname="Maxwell Kofi", lastname="Mensah"),
        EmployeeDB(firstname="Adolphe Boumsong", lastname="Dimouk"),
        EmployeeDB(firstname="Fabian", lastname="Dubaj"),
        EmployeeDB(firstname="Salh", lastname="Alamash"),
        EmployeeDB(firstname="Sarah Akuma", lastname="Ukpo"),
        EmployeeDB(firstname="Germay", lastname="Mehari"),
        EmployeeDB(firstname="Karolina", lastname="Włodarczyk"),
        EmployeeDB(firstname="Md Jowel", lastname="Hossain"),
        EmployeeDB(firstname="Renata", lastname="Molek"),
        EmployeeDB(firstname="Thaer", lastname="Al Gharib"),
        EmployeeDB(firstname="Kwame", lastname="Opoku"),
        EmployeeDB(firstname="Rawad", lastname="Al Akle")
    ]

    db_seed.add_all(employees_seed)
    db_seed.commit()

db_seed.close()

# ----------------------------------------------------
# APP
# ----------------------------------------------------

app = FastAPI(
    title="Doorline Rotation Manager",
    version="7.0.1"
)

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

# ----------------------------------------------------
# Stationen
# ----------------------------------------------------

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

double_takt_stations = {
    "40L", "40R",
    "50L", "50R",
    "60L", "60R",
    "70L", "70R"
}

# ----------------------------------------------------
# Datenbank Session
# ----------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------------------------------
# Home
# ----------------------------------------------------

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {
        "status": "running"
    }

# ----------------------------------------------------
# Employees
# ----------------------------------------------------

@app.get("/employees")
def get_employees(
        db: Session = Depends(get_db)
):
    return db.query(EmployeeDB).all()


@app.get("/employees/{employee_id}")
def get_employee(
        employee_id: int,
        db: Session = Depends(get_db)
):

    employee = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employee


@app.post("/employees")
def add_employee(
        employee: Employee,
        db: Session = Depends(get_db)
):

    employee_db = EmployeeDB(
        **employee.dict()
    )

    db.add(employee_db)
    db.commit()
    db.refresh(employee_db)

    return employee_db


@app.put("/employees/{employee_id}")
def update_employee(
        employee_id: int,
        employee: Employee,
        db: Session = Depends(get_db)
):

    employee_db = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if not employee_db:
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    for key, value in model_dump().items():
        setattr(employee_db, key, value)

    db.commit()
    db.refresh(employee_db)

    return employee_db


@app.delete("/employees/{employee_id}")
def delete_employee(
        employee_id: int,
        db: Session = Depends(get_db)
):

    employee_db = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if not employee_db:
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    db.delete(employee_db)
    db.commit()

    return {
        "message": "Mitarbeiter gelöscht"
    }

# ----------------------------------------------------
# Stations
# ----------------------------------------------------

@app.get("/stations")
def get_stations():
    return [
        {
            "name": station,
            "double_takt_allowed":
                station in double_takt_stations
        }
        for station in stations
    ]

# ----------------------------------------------------
# Rotation
# ----------------------------------------------------

@app.post("/rotation/run")
def run_rotation(
        db: Session = Depends(get_db)
):

    employees = db.query(EmployeeDB).all()

    rotation_result = []
    assigned_employees = set()
    support_employees = []

    for employee in employees:
        employee.station = None

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

            if employee.id in assigned_employees:
                continue

            if employee.last_station == station:
                continue

            if not getattr(
                    employee,
                    skill_name,
                    False
            ):
                continue

            assigned_employee = (
                f"{employee.firstname} "
                f"{employee.lastname}"
            )

            employee.last_station = employee.station
            employee.station = station
            employee.fairness_points += 1

            history = RotationHistory(
                employee_name=assigned_employee,
                station=station
            )

            db.add(history)

            assigned_employees.add(
                employee.id
            )

            break

        rotation_result.append({
            "name": station,
            "employee_1": assigned_employee,
            "employee_2": None,
            "support_required":
                assigned_employee is None,
            "double_takt_allowed":
                station in double_takt_stations
        })

    for employee in employees:

        if employee.is_sick:
            continue

        if employee.is_vacation:
            continue

        if employee.id not in assigned_employees:

            employee.station = "Support"

            support_employees.append(
                f"{employee.firstname} "
                f"{employee.lastname}"
            )

    db.commit()

    return {
        "message": "Rotation durchgeführt",
        "stations": rotation_result,
        "support_employees": support_employees
    }

# ----------------------------------------------------
# KPI
# ----------------------------------------------------

@app.get("/stats")
def stats(
        db: Session = Depends(get_db)
):

    employees = db.query(EmployeeDB).all()

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
        "double_takt": len(
            double_takt_stations
        )
    }

# ----------------------------------------------------
# Fairness
# ----------------------------------------------------

@app.get("/fairness")
def fairness(
        db: Session = Depends(get_db)
):

    employees = db.query(EmployeeDB).all()

    return {
        f"{e.firstname} {e.lastname}":
            e.fairness_points
        for e in employees
    }

# ----------------------------------------------------
# Historie
# ----------------------------------------------------

@app.get("/history")
def history(
        db: Session = Depends(get_db)
):

    return db.query(
        RotationHistory
    ).order_by(
        RotationHistory.id.desc()
    ).limit(100).all()

# ----------------------------------------------------
# Flexibility
# ----------------------------------------------------

@app.get("/flexibility")
def flexibility():

    return {
        "double_takt_stations":
            list(double_takt_stations)
    }
