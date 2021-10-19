import RPi.GPIO as GPIO
import time

from fastapi import FastAPI, HTTPException,status,Depends,APIRouter
from fastapi.responses import FileResponse
from typing import Optional

from app.schemas import member
from app.core import deps
from app.utils import response_code

from app.schemas import member
from app import pi_utils
import traceback

from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2


router = APIRouter()



# 初始化依赖
def init():
    try:
        f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return response_code.resp_500(
            message='指纹模块未初始化！',
            data=str(e)
        )
    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    return f

@router.get('/search',tags=['搜索指纹'])
def search(f=Depends(init)):
    ## Tries to search the finger and calculate hash
    try:
        # while  True:
            print('Waiting for finger...')

            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(FINGERPRINT_CHARBUFFER1)

            ## Searchs template
            result = f.searchTemplate()
            positionNumber = result[0]

            if ( positionNumber == -1 ):
                print('No match found!')
                return response_code.resp_202(
                data='未匹配到指纹'
            )
            else:
                print('Found template at position #' + str(positionNumber))
                return response_code.resp_200(
                    data={"finger_id": positionNumber}
                )
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return response_code.resp_500(
                    message='Operation failed!',
                    data=str(e)
                )

@router.post('/enroll',tags=['录入指纹'])
async def enroll(form:member.Members,f = Depends(init), db=Depends(deps.get_db)):
    print(form)
    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            return response_code.resp_202(
                data='该指纹已存在，该指纹ID为：' + str(positionNumber)
            )

        print('Keep for finger...')
        time.sleep(1)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(FINGERPRINT_CHARBUFFER2)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            print('finger don`t match')
            return response_code.resp_202(
                data='两次指纹不匹配'
            )

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        
        # 获取指纹特征数据
        characteristic = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)


        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        info = form.dict()
        info['finger_id'] = str(positionNumber)
        info['finger_data'] = str(characteristic)
        info = member.Member_info(**info)
        s = pi_utils.create_member_info(info)
        return response_code.resp_200(
            data=s
        )

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        traceback.print_exc()
        f.deleteTemplate(positionNumber)
        return response_code.resp_500(
            message='Operation failed!',
            data=str(e)
        )

@router.post('/delete_all',tags=['一键删除所有指纹'])
def delete_all(f = Depends(init)):
    r= f.clearDatabase()
    print(r)
    return response_code.resp_200(
        data=r
    )

@router.post('/delete',tags=['删除指纹'])
def delete(Id: int, f = Depends(init)):

    ## Tries to delete the template of the finger
    try:
        #positionNumber = input('Please enter the template position you want to delete: ')
        # positionNumber = int(positionNumber)
        positionNumber = Id

        if ( f.deleteTemplate(positionNumber) == True ):
            return response_code.resp_200(
                data=f"指纹模板删除成功！删除指纹ID为：{positionNumber}"
            )

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return response_code.resp_500(
                    message='Operation failed!',
                    data=str(e)
                )

@router.get('/index/{Id}', tags=['获取指纹模块使用情况'])
def index(Id: int = 0,f = Depends(init)):
    ## Tries to show a template index table page
    try:
        #page = input('Please enter the index page (0, 1, 2, 3) you want to see: ')
        page = Id

        tableIndex = f.getTemplateIndex(page)

        for i in range(0, len(tableIndex)):
            print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))
        return response_code.resp_200(
            data=tableIndex
        )
    except Exception as e:
        print('Operation failed!')
        return response_code.resp_500(
            message='Operation failed!',
            data=str(e)
        )

@router.post('/upload_data_by_name',tags=['上传指纹'])
def upload_data_by_name(data:member.upload_need, f = Depends(init)):
    """
    role:上传指纹数据
    """
    try:
          # for positionNumber in range(f.getTemplateCount()):

            positionNumber = int(data.finger_id)
            # print(positionNumber)
            f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)
            # Downloads the characteristics of template loaded in charbuffer 1
            characteristic = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)
           # print(characteristic)
            print(type(characteristic))
            # print(data)
            if info['finger_id']:
                print('enrolled successfully!')
                return response_code.resp_200(
                    data=info
                )
            else:
                print("enrolled Failed!")
                return {"data":"error"}
    except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            traceback.print_exc()
            #exit(1)



@router.get('/download',tags=['下载指纹'], description='## 用于下载指纹 ')
def download(name:str ,f = Depends(init)):
    try:
        # ID = int(input('请输入新成员的指纹ID：'))
    # for ID in range(44):
        data = utils.get_data(name)
        characteristic = eval(data["finger_data"])
        finger_id = int(data["finger_id"])
        print(finger_id, type(characteristic))
        t = f.uploadCharacteristics(FINGERPRINT_CHARBUFFER1, characteristic)
        if t:
            print("载入指纹数据成功！")
        else:
            print("载入指纹数据失败！")
            raise ValueError('The finger_data not download successfully!')
        positionNumber = f.storeTemplate(finger_id)
        # Downloads the characteristics of template loaded in charbuffer 1
        print('Now template position #' + str(positionNumber))
        time.sleep(0.5)
        print('enrolled successfully!')
        return {"data":"enrolled successfully!"}
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return response_code.resp_500(
            message='Operation failed!',
            data=str(e)
        )


@router.post('/mfrc_card',tags=['注册卡号'])
async def mfrc_register(form: member.Members):
    import traceback
    from mfrc522 import SimpleMFRC522
    # from pi_control import sound_1
    GPIO.setwarnings(False)
    # print(form)
    try:
        reader = SimpleMFRC522()
    except Exception as e:
        response_code.resp_202(
            data=str(e)
        )

    try:
        print('Waiting for your card...')
        card_id= reader.read_id()
        print(card_id)
        if card_id:
            info = form.dict()
            info['card_id'] = card_id
            print(info)
            response = pi_utils.create_member_info(**info)
            card_id =response['card_id']
            if card_id:
                # sound_1()
                print(f'注册成功，卡号为：{card_id}')
                return response_code.resp_200(
                    data=info
                )
    except Exception as e:
            traceback.print_exc()
            print(f'cuowu{str(e)}')
            return response_code.resp_500(
                data=str(e)
            )

@router.get('/query_pid',tags=['Utils'])
def query_pid(q: str = None):
    import os
    a = os.popen(f"ps -aux | grep {q}").readlines()

    return {"data":a}

@router.post('/kill',tags=['Utils'])
def kill(name: Optional[str] ='search'):
    import os
    a = os.system('sudo pkill -f ' +name)
    print(a)
    return {"data":a}
