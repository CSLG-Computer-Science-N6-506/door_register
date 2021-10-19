from datetime import datetime
from typing import List,Optional

from pydantic import BaseModel
from sqlalchemy import orm

class Record(BaseModel):
    time: datetime
    card_id : Optional[str] = None
    finger_id : Optional[str] = None

    class Config:
        orm_mode = True

class Members(BaseModel):
    id : str = None
    name : str = None
    stu_num : str = None
    phone : str = None
    card_id : str = None
    finger_id: str = None
    
    class Config:
        orm_mode = True


class user_info(BaseModel):
    name: str 
    stu_num: str
    class Config:
        orm_mode = True


class Record_enter(Record):
    name : Optional[str] = None

class Check_work(Record):
    name: Optional[str] = None
    class Config:
        orm_mode = True

class Check_work_list(Check_work):
    data : List[Check_work]
    class Config:
        orm_mode = True
class RecordCheck(Record_enter):
    
    check_work_attendance: Optional[bool] = None



class Member_info(Members):
    finger_data : str = None

class card_info(BaseModel):
    name: str = None
    card_id: str = None

class finger_id(BaseModel):
    finger_id: str = None
    name: str = None

    class Config:
        orm_mode = True

# 上传指纹数据

class upload_info(BaseModel):
    name : str = None
    finger_id: str = None
    finger_data: str = None
    
    class Config:
        orm_mode = True
    
class Date_input(BaseModel):
    start_date_time: datetime = datetime.now()
    end_date_time: datetime = datetime.now()

    class Config:
        orm_mode = True

class upload_need(BaseModel):
    name: str
    finger_id: str

class upload_data(upload_need):
    finger_data: str
    class Config:
        orm_mode=True