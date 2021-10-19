from typing import Optional

from pydantic import BaseModel, EmailStr, AnyHttpUrl


# Shared properties
class UserBase(BaseModel):
    # email: Optional[EmailStr] = None
    username: Optional[str] = None
    phone: int = None 
    is_active: Optional[bool] = True


class UserAuth(BaseModel):
    password: str


class UserNameAuth(UserAuth):
    username: str

# 手机号登录认证 验证数据字段都叫username
class UserPhoneAuth(UserAuth):
    username: int


# 创建账号需要验证的条件
class UserCreate(UserBase):
    nickname: str 
    # email: EmailStr
    username: str = 'admin'
    password: str = '123456'
    role_id: int
    avatar: 'AnyHttpUrl' = 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/qrcode/qrcode@2x-daf987ad02.png'


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


# 返回的用户信息
class UserInfo(BaseModel):
    role_id: int
    role: str
    nickname: str
    avatar: AnyHttpUrl
