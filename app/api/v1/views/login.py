from fastapi import APIRouter,status, Response

from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import Response

from app.schemas import login,info

router = APIRouter()

# 登录
@router.post('/login')
def login(form: login.Login):
    print(form)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': '200',  
            'message': 'sussess',
            'data': form.dict()
        }
    )


# 获取token
@router.get('/info')
def get_token(token: str):
    print(token)
    data = {
    'password': 'admin',
    'roles': ['admin'],
    'token': 'admin',
    'introduction': '我是超级管理员',
    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    'name': 'Super Admin'
    }
    print(type(data))
    data = info.Info(**data)
    print(data)
    return JSONResponse(
        status_code=200,
        content={
            'code': '200',
            'message': 'success',
            'data': data.dict()
        }
    )

# 注销登录

@router.post('/logout')
def logout(data:None):
    return JSONResponse(
        status_code=200,    
        content = {
            'code': '200',
            'message': 'success',
            'data': data if data else None
        }
    )