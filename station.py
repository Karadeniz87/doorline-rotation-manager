from pydantic import BaseModel
from typing import Optional


class Station(BaseModel):
    name: str

    active: bool = True

    double_takt_allowed: bool = False

    assigned_employee_1: Optional[str] = None
    assigned_employee_2: Optional[str] = None

    support_required: bool = False
