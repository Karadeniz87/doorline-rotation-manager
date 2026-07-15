from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from schemas import LoginRequest

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

    admin = db.query(EmployeeDB).filter(
        EmployeeDB.username == "admin"
    ).first()

    if admin is None:

        employees = [

    EmployeeDB(
        firstname="Onur",
        lastname="Yilmaz",
        username="admin",
        password="141187",
        role="admin"
    ),

    EmployeeDB(
        firstname="TL",
        lastname="SP",
        username="tlsp",
        password="tesla",
        role="teamlead_sp"
    ),

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
# Mitarbeiter zurücksetzen
# --------------------------------------------------

@app.get("/reset-employees")
def reset_employees(
    db: Session = Depends(get_db)
):

    db.query(EmployeeDB).delete()
    db.commit()

    seed_employees()

    return {
        "message": "Mitarbeiter erfolgreich zurückgesetzt"
    }


# --------------------------------------------------
# Doppelte Mitarbeiter löschen
# --------------------------------------------------

@app.get("/remove-duplicates")
def remove_duplicates(
    db: Session = Depends(get_db)
):
    employees = db.query(EmployeeDB).all()

    seen = set()
    deleted = 0

    for employee in employees:
        key = (
            employee.firstname.strip().lower(),
            employee.lastname.strip().lower()
        )

        if key in seen:
            db.delete(employee)
            deleted += 1
        else:
            seen.add(key)

    db.commit()

    return {
        "deleted_duplicates": deleted
    }


# --------------------------------------------------
# Login Page
# --------------------------------------------------

@app.get("/login-page")
def login_page():
    return FileResponse(
        "frontend/login.html"
    )


# --------------------------------------------------
# Login API
# --------------------------------------------------

@app.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(EmployeeDB).filter(
        EmployeeDB.username == request.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Benutzer nicht gefunden"
        )

    if user.password != request.password:
        raise HTTPException(
            status_code=401,
            detail="Falsches Passwort"
        )

    return {
        "success": True,
        "name": f"{user.firstname} {user.lastname}",
        "role": user.role
    }


@app.get("/create-tlsp")
def create_tlsp(
    db: Session = Depends(get_db)
):
    user = db.query(EmployeeDB).filter(
        EmployeeDB.username == "tlsp"
    ).first()

    if user:
        return {
            "message": "TLSP existiert bereits"
        }

    tlsp = EmployeeDB(
        firstname="TL",
        lastname="SP",
        username="tlsp",
        password="tesla",
        role="teamlead_sp"
    )

    db.add(tlsp)
    db.commit()

    return {
        "message": "TLSP erstellt"
    }
# --------------------------------------------------
# Admin Passwort zurücksetzen
# --------------------------------------------------

@app.get("/reset-admin")
def reset_admin(
    db: Session = Depends(get_db)
):
    admin = db.query(EmployeeDB).filter(
        EmployeeDB.username == "admin"
    ).first()

    if admin is None:
        return {
            "message": "Admin nicht gefunden"
        }

    admin.password = "141187"

    db.commit()

    return {
        "message": "Admin Passwort zurückgesetzt"
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
    double_takt_mode: bool = False,
    db: Session = Depends(get_db)
):
    employees = db.query(EmployeeDB).all()

    assigned_ids = set()
    rotation_result = []
    support_employees = []

    active_employees = [
        e for e in employees
        if not e.is_sick and not e.is_vacation
    ]

    available_count = len(active_employees)

    auto_double_takt = available_count < 15

    current_stations = (
        double_takt_layout
        if auto_double_takt or double_takt_mode
        else normal_stations
    )

    active_employees.sort(
        key=lambda x: x.fairness_points
    )

    # Ab hier ALLES 4 Leerzeichen eingerückt
    for station in current_stations:

        selected_employee = None

        for employee in active_employees:

            if employee.id in assigned_ids:
                continue

            if "+" in station:

                station_a, station_b = station.split("+")

                skill_a = f"skill_{station_a}"
                skill_b = f"skill_{station_b}"

                if employee.last_station == station:
    continue

if (
    getattr(employee, skill_a, False)
    and getattr(employee, skill_b, False)
):
    selected_employee = employee
    break

            else:

                skill_name = f"skill_{station}"

                if getattr(employee, skill_name, False):
                    selected_employee = employee
                    break
        if selected_employee:

            assigned_ids.add(selected_employee.id)

            selected_employee.station = station

            # -----------------------
            # Fairness Gewichtung
            # -----------------------
            weight = 1

            if "60" in station:
                weight = 2

            if "70" in station:
                weight = 2

            if "80" in station:
                weight = 3

            if "90" in station:
                weight = 2

            if "100" in station:
                weight = 2

            # Doppeltakt bekommt zusätzliche Punkte
            if "+" in station:
                weight += 2

            selected_employee.fairness_points += weight

            rotation_result.append({
                "station": station,
                "employee":
                    f"{selected_employee.firstname} "
                    f"{selected_employee.lastname}"
            })

        else:

            rotation_result.append({
                "station": station,
                "employee": None
            })

    # ------------------------------------
    # Nicht eingeplante Mitarbeiter
    # ------------------------------------
    for employee in active_employees:

        if employee.id not in assigned_ids:

            employee.station = "Support"

            support_employees.append(
                f"{employee.firstname} "
                f"{employee.lastname}"
            )

    # ------------------------------------
    # Besetzungsampel
    # ------------------------------------
    unassigned = sum(
        1 for s in rotation_result
        if s["employee"] is None
    )

    if unassigned == 0:
        staffing_status = "green"

    elif unassigned <= 2:
        staffing_status = "yellow"

    else:
        staffing_status = "red"

    db.commit()

    return {
        "message": "Rotation durchgeführt",
        "double_takt_mode": auto_double_takt,
        "available_employees": available_count,
        "stations": rotation_result,
        "support_employees": support_employees,
        "staffing_status": staffing_status
    }
    # --------------------------------------------------
# Stations API
# --------------------------------------------------

@app.get("/stations")
def get_stations(
    db: Session = Depends(get_db)
):

    employees = db.query(EmployeeDB).all()

    stations = []

    for station in normal_stations:

        employee = next(
            (
                e for e in employees
                if e.station == station
            ),
            None
        )

        stations.append({
            "station": station,
            "employee":
                f"{employee.firstname} {employee.lastname}"
                if employee else None
        })

    return stations
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
