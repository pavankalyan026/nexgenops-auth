from pydantic import BaseModel
from typing import Optional


class IndividualRegister(BaseModel):

    full_name: str

    email: str

    mobile: str

    password: str


class OrganizationRegister(BaseModel):

    organization_name: str
    organization_type: str
    official_email: str
    official_mobile: str
    country: str
    state: str
    city: str
    address: str
    employee_count: int

    owner_name: str
    designation: str
    owner_email: str
    owner_mobile: str

    password: str

    extra_data: str | None = None


class LoginSchema(BaseModel):

    organization_id: str | None = None

    email: str

    password: str