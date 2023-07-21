from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import get_session
from app.models import Division
from app.modules.divisions.schema import DivisionRead

router = APIRouter(prefix='/division')


@router.post('/create', status_code=status.HTTP_200_OK)
def add_division(
        division: str,
        db: Session = Depends(get_session)):
    division_add = Division(division=division)

    try:
        db.add(division_add)
        db.commit()
    except IntegrityError:
        db.rollback()
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    return division_add.to_dict()


@router.put('/delete', response_model=DivisionRead, status_code=status.HTTP_200_OK)
def delete_division(
        id: int,
        db: Session = Depends(get_session)):
    division_delete = db.get(Division, id)

    try:
        db.delete(division_delete)
        db.commit()
    except IntegrityError:
        db.rollback()
    return 'delete success'


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_division(
        id: int,
        db: Session = Depends(get_session)):
    division = db.get(Division, id)

    if not division:
        return status.HTTP_404_NOT_FOUND

    return division.to_dict()
