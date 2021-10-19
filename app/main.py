from fastapi import FastAPI,Request,Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api
from app.core.config import settings

import uvicorn

from app import pi_utils

app = FastAPI()


# 注册路由
app.include_router(api.api_router,
                #    prefix=settings.API_V1_STR
                   )


# 设置跨域请求

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
   import time
   pi_utils.buzzer_out()
   start_time = time.time()
   response = await call_next(request)
   process_time = time.time() - start_time
   print(process_time)
   response.headers["X-Process-Time"] = str(process_time)
   return response

# @app.middleware('http')
# async def dididi():
#     pi_utils.buzzer_out()

@app.get('/')
def root():
    return {"message": "Hello World!"}


