from pydantic import BaseModel


class EmployeeRead(BaseModel):
    id: int
    secondname: str
    firstname: str
    surname: str
    address: str
    date_of_birth: str


class EmployeeUpdate(BaseModel):
    secondname: str
    firstname: str
    surname: str
    address: str
    date_of_birth: str
