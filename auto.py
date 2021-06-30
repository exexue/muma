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
from aip import AipOcr

def ver_code():      #验证码识别获取
    '''
    通用文字识别（高精度版）
    '''
    client = AipOcr('***', '***', '***')

    ocr_file = ".\png\yzm.png"
    im = pyautogui.screenshot(region=(411, 347, 90 ,35))
    im.save(ocr_file)
    time.sleep(1)
    # 二进制方式打开图片文件
    f = open('.\png\yzm.png', 'rb')

    try:
        #  调用通用文字识别, 图片参数为本地图片 ,未定义识别参数
        result = client.basicAccurate(f.read())
        y = result['words_result'][0]['words']
        print(y)
        return y
    except:
        return 1
    
def _size(code,size):
    code_size = {'AL8888':5,'JD8888':10,'BU8888':10,'UR8888':10,'C8888':10,'M8888':10,'RM8888':10,'TA8888':5,
                  'MA8888':10,'FG8888':20,'PF8888':5,'SA8888':20,'FU8888':10,'CU8888':5,'ZN8888':5,'RB8888':10,'RU8888':10,
                  'HC8888':10,'SS8888':5,'P8888':10,'J8888':100,'Y8888':10,'JM8888':60,'I8888':100,'AP8888':10,'CJ8888':5,'SR8888':10,'CF8888':5
     }
    unit = code_size[code]
    x = int(size*(10/unit))
    return str(x)

def buy_open(code,size):
    pyautogui.click(705,303)
    time.sleep(2)
    pyautogui.hotkey('shift','ctrl','t')
    pyautogui.click(705,303)
    pyautogui.press('2')
    time.sleep(1)
    pyautogui.write(code,interval=0.3)
    pyautogui.press( 'enter' )
    pyautogui.press('1')
    pyautogui.press( 'enter' )
    pyautogui.press('1')
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.write("1",interval=0.3)
    pyautogui.press( 'tab' )
    pyautogui.press( 'tab' )
    #pyautogui.press( 'enter' )
    #pyautogui.press( 'enter' )
    pyautogui.hotkey('winleft','d')   #窗口最小化
    return 1
    

    
    

def sell_open(code,size):
    pyautogui.click(705,303)
    time.sleep(2)
    pyautogui.hotkey('shift','ctrl','t')
    pyautogui.click(705,303)
    pyautogui.press('2')
    time.sleep(1)
    pyautogui.write(code,interval=0.3)
    pyautogui.press( 'enter' )
    pyautogui.press('2')
    pyautogui.press( 'enter' )
    pyautogui.press('1')
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.write("1",interval=0.3)
    pyautogui.press( 'tab' )
    pyautogui.press( 'tab' )
    #pyautogui.press( 'enter' )
    #pyautogui.press( 'enter' )
    pyautogui.hotkey('winleft','d')
    return 1
    
def sell_close(code,size):
    pyautogui.click(705,303)
    time.sleep(2)
    pyautogui.hotkey('shift','ctrl','t')
    pyautogui.click(705,303)
    pyautogui.press('2')
    time.sleep(1)
    pyautogui.write(code,interval=0.3)
    pyautogui.press( 'enter' )
    pyautogui.press('2')
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.press('2')
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.write("1",interval=0.3)
    pyautogui.press( 'tab' )
    pyautogui.press( 'tab' )
    #pyautogui.press( 'enter' )
    #pyautogui.press( 'enter' )
    pyautogui.hotkey('winleft','d')
    return 0
    
def buy_close(code,size):
    pyautogui.click(705,303)
    time.sleep(2)
    pyautogui.hotkey('shift','ctrl','t')
    pyautogui.click(705,303)
    pyautogui.press('2')
    time.sleep(1)
    pyautogui.write(code,interval=0.3)
    pyautogui.press( 'enter' )
    pyautogui.press('1')
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.press('2')
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.write("1",interval=0.3)
    pyautogui.press( 'tab' )
    pyautogui.press( 'tab' )
    #pyautogui.press( 'enter' )
    #pyautogui.press( 'enter' )
    pyautogui.hotkey('winleft','d') 
    return 0
        

    
def open_trade():
    #start = pyautogui.locateCenterOnScreen('.\png\start.png')
    #pyautogui.click(start)
    pyautogui.click(80,575)
    
    #pyautogui.click()
    time.sleep(3)
    pyautogui.press( 'enter' )
    time.sleep(2)
    print("打开交易软件成功。")
    pyautogui.write("*********",interval=0.3)
    pyautogui.press( 'tab' )
    ver_txt= ver_code()
    time.sleep(1)
    pyautogui.write(ver_txt,interval=0.3)
    time.sleep(1)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.press( 'enter' )
    time.sleep(15)
    login = pyautogui.locateCenterOnScreen('.\png\cash.png')
    if login is not None:
        print(login)
        print("登录成功了...")
        #pyautogui.click(login)
        pyautogui.press( 'enter' )
        #buy_open('C2109','100')
    else:
        print("登录失败,结束进程...")
        os.system('tskill STradeClient')
        time.sleep(1)
        os.system('python c:\autotrade.py')
            

            
# buy('510500','100')
# time.sleep(1)
# sell('510500','100')
if __name__ == "__main__":
    #buy_close('C2109','100')
    
    date = datetime.datetime.now().date()
    h = int(time.strftime("%H"))  
    if is_workday(date):
        print("是工作日")
        if h >=8 and h <=12  or h>=13 and h<=20  or h >= 21 and h <= 23 :
            print("当前为交易时间")
            process = os.popen("tasklist")
            txt = process.read()
            if 'STradeClient' in txt :
                print("进程已经存在了")
                login = pyautogui.locateCenterOnScreen('.\png\cash.png')
                if login is not None:
                    print(login)                        #窗口已经最大化了
                else:
                    pyautogui.click(80,575)     #窗口最大化
                    
            else:
                open_trade()   #如果进程不存在并且在交易时间内就再次打开。
                
                
                



    else:
        print("是休息日")


# ## 

# In[29]:

