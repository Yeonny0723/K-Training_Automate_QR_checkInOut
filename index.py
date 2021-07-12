# Post 로그인 요청
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time

load_dotenv()

# 로그인 Post 요청
headers = {
    'User-Agent': '	multipart/form-data; boundary=----WebKitFormBoundaryzYSkLhgcbqLdnGvm'
}
url = 'https://m.hrd.go.kr/hrdm/mb/mmbao/login.do'
data = {
    'loginId':os.getenv('loginId'), 
    'loginPwd':os.getenv('loginPwd'),
    'autoLoginSe': 'Y'
}

response = requests.post(url,data,headers)
print('Login result : ',response.content)

# Post 입실 요청 ----------------------------------------------
headers = {
    'User-Agent':os.getenv('user_agent')
}

# def checkIn():

# Post 퇴실 요청 ----------------------------------------------
def checkOut():
    url = 'https://m.hrd.go.kr/hrdm/qr/at/sendQrAttend.do'
    data = {
        'trpr_id':'AIG20200000288892',
        'tracseId':'AIG20200000288892',
        'trpr_degr':'8',
        'tracseTme':'8',
        'trpr_gbn_cd':'C0061',
        'crseTracseSe':'C0061',
        'trp_id':'100045274633',
        'trneeCstmrId':'100045274633',
        'latitude':os.getenv('latitude'),
        'longitude':os.getenv('longitude'),
        'qr_string':os.getenv('qr_string'),
        'uuid':os.getenv('uuid'),
        'retirYn': 'N',
        'in_retir_gbn': 'O',
        'lpslvrSe':'O',
        'appVer':'HRDNET-APP V3.0'
    }
    response = requests.post(url,data,headers)
    if (response.status_code == 200):
        print('체크아웃 되었습니다')
        print('Result : ',response.content) #
    else:
        print('다시 시도해주세요')



# 자동 오전 9시-입실, 오후 5시 퇴실  -----------------------------

def weekday_job(x, t=None):
    week = datetime.today().weekday() # 0 - Mon... 6-Sun
    if t is not None and week < 5:
        schedule.every().day.at(t).do(x)

# weekday_job(checkIn, '09:00')
weekday_job(checkOut, '17:00')

while True:
    schedule.run_pending()
    time.sleep(60)    

# code referred from: 'https://stackoverflow.com/questions/47086739/python-scheduling-a-job-starting-every-weekday-and-running-every-hour'