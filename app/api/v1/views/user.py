#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/7 14:11
# @Author  : CoderCharm
# @File    : views.py
# @Software: PyCharm
# @Desc    :
"""

"""
from datetime import timedelta
from typing import Any, Optional

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header

from app.core import deps
from app.utils import response_code

from app.models import auth
from app.core.config import settings
from app.core import security

from app.schemas import user
from app.crud import curd_user, curd_role

router = APIRouter()


@router.post("/login/access-token", summary="用户登录认证")
async def login_access_token(
        *,
        db: Session = Depends(deps.get_db),
        user_info: user.UserNameAuth,
        user_agent: Optional[str] = Header(None)
) -> Any:
    """
    用户登录
    :param db:
    :param user_info:
    :param user_agent:
    :return:
    """
    print(user_info.dict())
    # 验证用户
    user = curd_user.authenticate(
        db, username=user_info.username, password=user_info.password)
    if not user:
        return response_code.resp_500(message="用户名或者密码错误")
    elif not curd_user.is_active(user):
        return response_code.resp_500(message="用户邮箱未激活")

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TAKEN_EXPIRE_MINUTES)

    return response_code.resp_200(data={
        "token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "Bearer",
    })

@router.post('/user/create')
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_info: user.UserCreate
):
    print(user_info)
    user = curd_user.create(db, obj_in=user_info)
    return user


@router.get("/user/info", summary="获取用户信息", response_model=user.UserInfo)
async def get_user_info(
        *,
        db: Session = Depends(deps.get_db),
        current_user: auth.AdminUser = Depends(deps.get_current_user)
) -> Any:
    """
    获取用户信息
    :param db:
    :param current_user:
    :return:
    """
    role_info = curd_role.query_role(db, role_id=current_user.role_id)

    return response_code.resp_200(data={
        "role_id": current_user.role_id,
        "role": role_info.role_name,
        "nickname": current_user.nickname,
        "avatar": current_user.avatar
    })


@router.post("/user/logout", summary="用户退出")
async def user_logout(current_user: auth.AdminUser = Depends(deps.get_current_user)):
    """
    用户退出
    :param current_user:
    :return:
    """
    return response_code.resp_200(data="ok")


@router.get("/table/list", summary="临时table_list接口")
async def test_table_list():
    return response_code.resp_200(data={
        "items": [
            {
                "id": '530000198812025837',
                "title": '标题11111',
                "status": 'published',
                "author": '作者1',
                "display_time": '2011-06-09 04:49:53',
                "pageviews": 2540
            },
            {
                "id": '222222222222',
                "title": '标题2222',
                "status": 'draft',
                "author": '作者2',
                "display_time": '2011-06-09 04:49:53',
                "pageviews": 2540
            },
            {
                "id": '33333',
                "title": '标题33333',
                "status": 'deleted',
                "author": '作者3333',
                "display_time": '2011-06-09 04:49:53',
                "pageviews": 2540
            }
        ]
    })


