from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.models.auth import AdminUser

class CRUDUser(CRUDBase[AdminUser, UserCreate, UserUpdate]):

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[AdminUser]:
        return db.query(AdminUser).filter(AdminUser.email == email).first()

    @staticmethod
    def get_by_username(db: Session, *, username: str) -> Optional[AdminUser]:
        return db.query(AdminUser).filter(AdminUser.email == username).first()


    def create(self, db: Session, *, obj_in: UserCreate) -> AdminUser:
        db_obj = AdminUser(
            nickname=obj_in.nickname,
            email=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            role_id=obj_in.role_id,
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[AdminUser]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: AdminUser) -> bool:
        return user.is_active

    def is_superuser(self, user: AdminUser) -> bool:
        return user.is_superuser


curd_user = CRUDUser(AdminUser)
