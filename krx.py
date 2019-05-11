import pandas as pd
import numpy as np
import requests
from io import BytesIO
from datetime import datetime, timedelta

def get_daily_price(code, fromdate=None, todate=None):
    if todate == None:
        todate = datetime.today().strftime('%Y%m%d')   # 오늘 날짜

    if fromdate == None:
        fromdate = (datetime.today() - timedelta(days=30)).strftime('%Y%m%d')   # 30일 이전 날짜

    # STEP 01: Generate OTP
    gen_otp_url = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx"
    gen_otp_data = {
        'name':'fileDown',
        'filetype':'csv',
        'url':'MKD/04/0402/04020100/mkd04020100t3_02',
        'isu_cd':code,
        'fromdate':fromdate,
        'todate':todate,
    }
    
    r = requests.post(gen_otp_url, gen_otp_data)
    code = r.content  # 리턴받은 값을 아래 요청의 입력으로 사용.
    
    # STEP 02: download
    down_url = 'http://file.krx.co.kr/download.jspx'
    down_data = {
        'code': code,
    }
    
    r = requests.post(down_url, down_data)
    r.encoding = "utf-8-sig"
    df = pd.read_csv(BytesIO(r.content), header=0, thousands=',')
    return df
df = get_daily_price('KR7035420009')
df.head()
