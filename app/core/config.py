import secrets
from typing import List

from pydantic import BaseSettings

class Settings(BaseSettings):
    """
        配置类
    """

    # 项目地址
    # API_V1_STR: str = "/api/v1"
    
    API_V1_STR: str = "/api/admin/v1"


    # taken 相关
    ALGORITHM: str = "HS256" # 加密算法
    SECRET_KEY: str = secrets.token_urlsafe(32) # 随机生成的base64位字符串
    ACCESS_TAKEN_EXPIRE_MINUTES: int = 60*24*3 # taken的时效 3天 = 60*24*3

    # 跨域设置
    ORIGINNS: List[str] = ['*',] 

    # 静态文件
    STATIC_DIR = "static"
    
    # mysql数据库相关设置
    MYSQL_USERNAME: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_HOST: str = "10.18.55.156"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "lab_door"

    # Mysql地址
    SQLALECHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@"\
                               f"{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"
    
    # redis 配置
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PASSWORD: str = "123456"
    REDIS_DB: int = 8
    REDIS_PORT: int = 6379
    REDIS_TIME_OUT = 5 * 60 * 60    # 缓存时间默认三小时
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encodind=utf-8"

settings = Settings()
