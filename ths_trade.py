#!/usr/bin/env python
# coding: utf-8

# In[17]:


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
# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MWTCUxZYC1MGjWe9NLwvQYja&client_secret=5tbSErlUvgp3aR64RbflqxSGbP6PUcpV'
# response = requests.get(host)
# if response:
#     print(response.json())
def ver_code():      #验证码识别获取
    '''
    通用文字识别（高精度版）
    '''

    ocr_file = ".\png\yzm.png"
    im = pyautogui.screenshot(region=(411, 347, 90 ,35))
    im.save(ocr_file)
    time.sleep(1)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open('.\png\yzm.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token ='24.b1c808959c14ab1942f8904b2890df69.2592000.1624007696.282335-24203735'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(request_url, data=params, headers=headers)
    except:
        time.sleep(6)
        print("cooncet Baidu erro ... ")
        response = requests.post(request_url, data=params, headers=headers)
    try:
        if response:
            print (response.json())
        x = response.json()
        y = x['words_result'][0]['words']
        print(y)
        return y
    except:
        return 1
    


def buy(code,size):
    time.sleep(2)
    pyautogui.press( 'f1' )
    time.sleep(1)
    pyautogui.write(code,interval=0.3)
    pyautogui.press( 'tab' )
    time.sleep(1)
    pyautogui.write(size,interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(2)
    pyautogui.press( 'enter' )
    return 1
    
    

    
    

def sell(code,size):
    time.sleep(2)
    pyautogui.press( 'f2' )
    time.sleep(1)
    pyautogui.write(code,interval=0.3)
    pyautogui.press( 'tab' )
    time.sleep(1)
    pyautogui.write(size,interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(2)
    pyautogui.press( 'enter' )
    return 0
    

    
def open_trade():
    #start = pyautogui.locateCenterOnScreen('.\png\start.png')
    #pyautogui.click(start)
    pyautogui.click(39,29)
    pyautogui.click()
    time.sleep(8)   
    process = os.popen("tasklist /v")
    txt = process.read()
    if '网上股票交易系统5.0' in txt :
        print("自动登录成功了...")
        pyautogui.press( 'f1' )
        pyautogui.hotkey('winleft', 'up')
        
        
        #sell('510500','100')
        
    else:
        print("自动登录失败,开始手动登录")
        time.sleep(3)
        pyautogui.press( 'enter' )
        time.sleep(5)
        process = os.popen("tasklist /v")
        txt = process.read()
        if '网上股票交易系统5.0' in txt :
            print("手动登录成功了...")
            pyautogui.press( 'f1' )
            pyautogui.hotkey('winleft', 'up')
        else:
            print("手动登录失败,结束进程...")
            os.system('tskill xiadan')
            time.sleep(1)
                

            
if __name__ == "__main__":
    time.sleep(2)
    
    date = datetime.datetime.now().date()
    h = int(time.strftime("%H"))  
    if is_workday(date):
        print("是工作日")
        if h >=9 and h <=18:
            print("当前为交易时间")
            process = os.popen("tasklist")
            txt = process.read()
            if 'xiadan' in txt :
                print("THS_进程已经存在了")
            else:
                open_trade()   #如果进程不存在并且在交易时间内就再次打开。
                
                
                



    else:
        print("是休息日")
        open_trade() 


# ## 

# In[29]:
