from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    firstname: str
    lastname: str
    status: str = "Verfügbar"

    station: Optional[str] = None

    skill_30L: bool = False
    skill_30R: bool = False
    skill_40L: bool = False
    skill_40R: bool = False
    skill_50L: bool = False
    skill_50R: bool = False
    skill_60L: bool = False
    skill_60R: bool = False
    skill_70L: bool = False
    skill_70R: bool = False
    skill_80L: bool = False
    skill_80R: bool = False
    skill_90L: bool = False
    skill_90R: bool = False
    skill_100L: bool = False
    skill_100R: bool = False
    skill_110L: bool = False
    skill_110R: bool = False

    fairness_points: int = 0
