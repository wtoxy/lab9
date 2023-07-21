from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import get_session
from app.models import Job
from app.modules.job.schema import JobRead, Employment, Dismissal

router = APIRouter(prefix='/job')


@router.post('/employment', response_model=JobRead, status_code=status.HTTP_200_OK)
def employment(
        data: Employment,
        db: Session = Depends(get_session)):
    new_employee = Job(**data.dict())

    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
    except IntegrityError:
        db.rollback()
        return JobRead(
            error='No employee',
            **new_employee.to_dict())

    return JobRead(
        employee=new_employee.employee.to_dict(),
        **new_employee.to_dict())


@router.put('/dismissal', response_model=JobRead, status_code=status.HTTP_200_OK)
def dismissal(
        id: int,
        data: Dismissal,
        db: Session = Depends(get_session)):

    dismissal_employee = db.get(Job, id)

    values = data.dict()
    dismissal_employee.update(**values)

    try:
        db.add(dismissal_employee)
        db.commit()
    except IntegrityError:
        db.rollback()

    return dismissal_employee.to_dict()
