from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.models.members import Members

class CRUDUser(CRUDBase[Members, UserCreate, UserUpdate]):
    def get_members(self,db: Session):
        return db.query(Members).all()





curd_member = CRUDUser(Members)
