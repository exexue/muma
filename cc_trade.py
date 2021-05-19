import os
#os.environ['DISPLAY'] = ':2'
import pyautogui
import time
import datetime
from chinese_calendar import is_workday
# encoding:utf-8

import requests
import base64

# # client_id 为官网获取的AK， client_secret 为官网获取的SK
# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_cred**************'
# response = requests.get(host)
# if response:
#     print(response.json())
def ver_code():      #验证码识别获取
    '''
    通用文字识别（高精度版）
    '''
    ocr_file = "/root/yzm.png"
    im = pyautogui.screenshot(region=(650, 350, 70 ,40))
    im.save(ocr_file)
    time.sleep(1)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open('/root/yzm.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token ='24.*******************'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())
    x = response.json()
    y = x['words_result'][0]['words']
    print(y)
    return y


def buy(code,size):
    login = pyautogui.locateCenterOnScreen('/root/buy.png')
    pyautogui.click(login)
    time.sleep(2)
    pyautogui.write(code,interval=0.3)
    time.sleep(1)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.write(size,interval=0.3)
    time.sleep(1)
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.press( 'enter' )
    my = pyautogui.locateCenterOnScreen('/root/my.png')
    pyautogui.click(my)

def sell(code,size):
    login = pyautogui.locateCenterOnScreen('/root/sell.png')
    pyautogui.click(login)
    time.sleep(2)
    pyautogui.write(code,interval=0.3)
    time.sleep(1)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.write(size,interval=0.3)
    time.sleep(1)
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.press( 'enter' )
    my = pyautogui.locateCenterOnScreen('/root/my.png')
    pyautogui.click(my)    
    
def open_trade():
    os.system('wine "/root/.wine/drive_c/Program Files (x86)/CFT5/bin/cft5.exe "& ')
    time.sleep(35)
    start = pyautogui.locateCenterOnScreen('/root/logo.png')
    if start == None:
        print("打开交易软件失败。")
    else:
        print("打开交易软件成功。")
        pyautogui.write("********")
        pyautogui.press( 'tab' )
        ver_txt= ver_code()
        pyautogui.write(ver_txt)
        pyautogui.press( 'enter' )
        time.sleep(15)
        login = pyautogui.locateCenterOnScreen('/root/buy.png')
        if login is not None:
            print(login)
            print("登录成功了...")
            #pyautogui.click(login)
        else:
            print("登录失败,结束进程...")
            os.system('killall -r cft5.exe')    

            
# buy('510500','100')
# time.sleep(1)
# sell('510500','100')
if __name__ == "__main__":
    
    date = datetime.datetime.now().date()
    h = int(time.strftime("%H"))  
    if is_workday(date):
        print("是工作日")
        if h >=9 and h <=11  or h>=13 and h<=21:
            print("当前为交易时间")
            process = os.popen("ps -x |grep cft5")
            txt = process.read()
            if 'cft5.exe' in txt :
                print("进程已经存在了")
            else:
                open_trade()   #如果进程不存在并且在交易时间内就再次打开。



    else:
        print("是休息日")

