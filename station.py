from pydantic import BaseModel
from typing import Optional


class Station(BaseModel):
    name: str

    active: bool = True

    double_takt: bool = False

    assigned_employee_left: Optional[str] = None
    assigned_employee_right: Optional[str] = None

    support_required: bool = False
