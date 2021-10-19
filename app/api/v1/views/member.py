from datetime import timedelta
from typing import Any, Optional

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from app import schemas

from app.core import deps
from app.utils import response_code

from app.models import auth,members
from app.core.config import settings
from app.core import security

from app.schemas import user,member
from app.crud import curd_user, curd_member

router = APIRouter()

@router.get('/members')
def get_members(db:Session= Depends(deps.get_db)):
    data = curd_member.get_members(db)
    data_list = [i.dobule_to_dict() for i in data]
    # print(data_list)
    return response_code.resp_200(
        data=data_list
    )


