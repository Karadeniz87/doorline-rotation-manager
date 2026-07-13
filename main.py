from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import EmployeeDB, RotationHistory

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doorline Rotation Manager",
    version="11.0.0"
)

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

# --------------------------------------------------
# Mitarbeiter automatisch anlegen
# --------------------------------------------------

def seed_employees():

    db = SessionLocal()

    if db.query(EmployeeDB).count() == 0:

        employees = [
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

        db.add_all(employees)
        db.commit()

    db.close()


seed_employees()

# --------------------------------------------------
# Stationen
# --------------------------------------------------

double_takt_mode = False

normal_stations = [
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

double_takt_layout = [
    "30L", "30R",
    "40L+50L",
    "40R+50R",
    "60L+70L",
    "60R+70R",
    "80L", "80R",
    "90L", "90R",
    "100L", "100R",
    "110L", "110R"
]
# --------------------------------------------------
# Datenbank Session
# --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {
        "status": "running"
    }


# ----------------------------------------------------
# Double Takt
# ----------------------------------------------------

double_takt_mode = False


@app.get("/double-takt")
def get_double_takt():
    return {
        "enabled": double_takt_mode
    }


@app.post("/double-takt/toggle")
def toggle_double_takt():
    global double_takt_mode

    double_takt_mode = not double_takt_mode

    return {
        "enabled": double_takt_mode
    }

# --------------------------------------------------
# Employees
# --------------------------------------------------

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

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employee


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee_data: dict,
    db: Session = Depends(get_db)
):

    employee = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    for key, value in employee_data.items():

        if hasattr(employee, key):
            setattr(
                employee,
                key,
                value
            )

    db.commit()
    db.refresh(employee)

    return employee


@app.post("/employees")
def add_employee(
    employee_data: dict,
    db: Session = Depends(get_db)
):

    employee = EmployeeDB(
        **employee_data
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(EmployeeDB).filter(
        EmployeeDB.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Mitarbeiter gelöscht"
    }

# --------------------------------------------------
# Rotation
# --------------------------------------------------

double_takt_stations = {
    "40L",
    "40R",
    "50L",
    "50R",
    "60L",
    "60R",
    "70L",
    "70R"
}


@app.post("/rotation/run")
def run_rotation(
    db: Session = Depends(get_db)
):

    employees = db.query(EmployeeDB).all()

    assigned_ids = set()
    rotation_result = []
    support_employees = []

        active_employees = [
        e for e in employees
        if not e.is_sick
        and not e.is_vacation
    ]

    available_count = len(active_employees)

    # Automatischer Double-Takt bei Unterbesetzung
    auto_double_takt = available_count < 15

    current_stations = (
        double_takt_layout
        if auto_double_takt or double_takt_mode
        else normal_stations
    )

active_employees.sort(
    key=lambda x: x.fairness_points
    )

    for station in current_stations:

        selected_employee = None

        # Skillname bestimmen
        if "+" in station:
            base_station = station.split("+")[0]
            skill_name = f"skill_{base_station}"
        else:
            skill_name = f"skill_{station}"

        for employee in active_employees:

            if employee.id in assigned_ids:
                continue

            if hasattr(employee, skill_name):
                if not getattr(employee, skill_name):
                    continue

            selected_employee = employee

            assigned_ids.add(employee.id)

            employee.last_station = employee.station
            employee.station = station
            employee.fairness_points += 1

            db.add(
                RotationHistory(
                    employee_name=f"{employee.firstname} {employee.lastname}",
                    station=station
                )
            )

            break

        rotation_result.append(
            {
                "name": station,

                "employee_1":
                    f"{selected_employee.firstname} {selected_employee.lastname}"
                    if selected_employee else None,

                "employee_2": None,

                "support_required":
                    selected_employee is None,

                "double_takt_allowed":
                    (
                        "40" in station
                        or "50" in station
                        or "60" in station
                        or "70" in station
                    )
            }
        )

    for employee in active_employees:

        if employee.id not in assigned_ids:

            employee.station = "Support"

            support_employees.append(
                f"{employee.firstname} {employee.lastname}"
            )

    db.commit()

    return {
    "message": "Rotation durchgeführt",
    "double_takt_mode": auto_double_takt or double_takt_mode,
    "available_employees": available_count,
    "stations": rotation_result,
    "support_employees": support_employees
}
# --------------------------------------------------
# KPI
# --------------------------------------------------

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

    return {
        "employees_total":
            len(employees),

        "available":
            len(employees)
            - sick
            - vacation,

        "vacation":
            vacation,

        "sick":
            sick,

        "support":
            support,

        "double_takt":
            len(double_takt_stations)
    }

# --------------------------------------------------
# Fairness
# --------------------------------------------------

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

# --------------------------------------------------
# Historie
# --------------------------------------------------

@app.get("/history")
def history(
    db: Session = Depends(get_db)
):

    return db.query(
        RotationHistory
    ).order_by(
        RotationHistory.id.desc()
    ).limit(100).all()

# --------------------------------------------------
# Flexibility
# --------------------------------------------------

@app.get("/flexibility")
def flexibility():

    return {
        "double_takt_stations":
            double_takt_stations
    }
