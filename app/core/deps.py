from typing import Generator, Optional

from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings

from app.models import auth
from app.utils import custom_exc
from app import schemas

from app import crud


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)



def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: Optional[str] = Header(None)
) -> auth.AdminUser:
    if not token:
        raise custom_exc.UserTokenError(err_desc='headers not found token')
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
        print(token_data)
    except (jwt.JWTError, ValidationError):
        raise custom_exc.UserTokenError(err_desc="access token fail")
    user = crud.curd_user.get(db, id=token_data.sub)
    print(user)
    if not user:
        raise custom_exc.UserNotFound(err_desc="user not found")
    return user

