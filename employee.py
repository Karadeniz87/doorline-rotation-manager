from pydantic import BaseModel


class Employee(BaseModel):
    firstname: str
    lastname: str

    status: str = "Verfügbar"

    fairness_points: int = 0

    skill_30L: int = 3
    skill_30R: int = 3

    skill_40L: int = 3
    skill_40R: int = 3

    skill_50L: int = 3
    skill_50R: int = 3

    skill_60L: int = 3
    skill_60R: int = 3

    skill_70L: int = 3
    skill_70R: int = 3

    skill_80L: int = 3
    skill_80R: int = 3

    skill_90L: int = 3
    skill_90R: int = 3

    skill_100L: int = 3
    skill_100R: int = 3

    skill_110L: int = 3
    skill_110R: int = 3
