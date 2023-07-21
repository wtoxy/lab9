from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import get_session
from app.models import Position
from app.modules.positions.schema import PositionRead

router = APIRouter(prefix='/position')


@router.post('/create', status_code=status.HTTP_200_OK)
def add_position(
        position: str,
        db: Session = Depends(get_session)):
    position_add = Position(position=position)

    try:
        db.add(position_add)
        db.commit()
    except IntegrityError:
        db.rollback()
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    return position_add.to_dict()


@router.put('/delete', response_model=PositionRead, status_code=status.HTTP_200_OK)
def delete_position(
        id: int,
        db: Session = Depends(get_session)):
    position = db.get(Position, id)

    try:
        db.delete(position)
        db.commit()
    except IntegrityError:
        db.rollback()
    return 'delete success'


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_position(
        id: int,
        db: Session = Depends(get_session)):
    position = db.get(Position, id)

    if not position:
        return status.HTTP_404_NOT_FOUND

    return position.to_dict()
