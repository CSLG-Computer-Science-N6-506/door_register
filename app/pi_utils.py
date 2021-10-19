import RPi.GPIO as GPIO
import time



import requests
import json
import time
from app import schemas

from fastapi.encoders import jsonable_encoder


from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1


buzzer_pin = 11

def buzzer_out():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(buzzer_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(buzzer_pin,1)
    time.sleep(0.5)
    GPIO.output(buzzer_pin,0)
    GPIO.cleanup()




def search_finger():
    try:
        f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to search the finger and calculate hash
    while True:
        try:
            print('Waiting for finger...')
            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(FINGERPRINT_CHARBUFFER1)

            ## Searchs template
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber == -1 ):
                print('No match found!')
                # exit(0)
            else:
                print('Found template at position #' + str(positionNumber))


        except Exception as e:
            # print('Operation failed!')
            # print('Exception message: ' + str(e))
            # exit(1)
            pass


# url="http://127.0.0.1:8001"
url="http://10.18.52.156:9009"



def send_data(finger_id=None,card_id=None):
    date_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    data={
          "recv":
             {
          "time": date_time,
          "finger_id": finger_id,
          "card_id": card_id,
          "name": "string"
          },
          "check_work_attendance": True
}
    data = json.dumps(data)
    # print(data)
    r = requests.post(url+"/auth/",data=data)
    recv = json.loads(r.text)
    print(recv,type(recv))
    return recv

def create_member_info(info=schemas.Member_info):
     print(info.dict())
     data = json.dumps(info.dict())
     if not info.card_id:
        recv = requests.post(url+"/finger_enroll",data=data)
     else:
        data = json.dumps(schemas.card_info(**info.dict()).dict())
        recv= requests.post(url+"/update_card_id",data=data)
     recv = json.loads(recv.text)
     print(recv)
     return recv

def get_data(name:str):
     url_info = url+"/user_data?name={}".format(name)
     print(url_info)
     r = requests.get(url_info)
     recv = json.loads(r.text)
     print(recv)
     return recv
    

def upload_data(data: schemas.upload_data):
    data = jsonable_encoder(data)
    data = json.dumps(data)
    print(type(data))
    r= requests.post(url=url+'/upload_data',data=data)
    r = json.loads(r.text)
    print(r)
    return r


def delete_finger(id: int):
    r= requests.post(url=url+'/upload_data',data=id)
    print(r)
    r = json.loads(r.text)
    print(r)
    return r

# 考勤
def check_work_attendance():
    pass