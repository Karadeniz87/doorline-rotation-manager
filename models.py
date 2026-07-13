from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime

from database import Base


class EmployeeDB(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True, nullable=True)
password = Column(String, nullable=True)
role = Column(String, default="teamlead")

    station = Column(String, nullable=True)
    last_station = Column(String, nullable=True)

    fairness_points = Column(Integer, default=0)

    is_sick = Column(Boolean, default=False)
    is_vacation = Column(Boolean, default=False)

    skill_30L = Column(Boolean, default=False)
    skill_30R = Column(Boolean, default=False)

    skill_40L = Column(Boolean, default=False)
    skill_40R = Column(Boolean, default=False)

    skill_50L = Column(Boolean, default=False)
    skill_50R = Column(Boolean, default=False)

    skill_60L = Column(Boolean, default=False)
    skill_60R = Column(Boolean, default=False)

    skill_70L = Column(Boolean, default=False)
    skill_70R = Column(Boolean, default=False)

    skill_80L = Column(Boolean, default=False)
    skill_80R = Column(Boolean, default=False)

    skill_90L = Column(Boolean, default=False)
    skill_90R = Column(Boolean, default=False)

    skill_100L = Column(Boolean, default=False)
    skill_100R = Column(Boolean, default=False)

    skill_110L = Column(Boolean, default=False)
    skill_110R = Column(Boolean, default=False)


class RotationHistory(Base):

    __tablename__ = "rotation_history"

    id = Column(Integer, primary_key=True, index=True)

    employee_name = Column(String)

    station = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )
