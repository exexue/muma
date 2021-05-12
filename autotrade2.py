#!/usr/bin/env python
# coding: utf-8

# In[14]:


#!/usr/bin/env python
# coding: utf-8

# In[14]:
import time,os
os.environ['DISPLAY'] = ':2'
import pyautogui
import datetime


# 合约输入60,325 ，买入按钮53,355，卖出按钮101，356 ，开仓按钮54，378 ，平仓按钮149，378
# 手数输入91，410，指定价输入95，443 ，市价按钮62，477，下单按钮100，488

def _size(code,size):
    code_size = {'AL8888':5,'JD8888':10,'BU8888':10,'UR8888':10,'C8888':10,'M8888':10,'RM8888':10,'TA8888':5,
                  'MA8888':10,'FG8888':20,'PF8888':5,'SA8888':20,'FU8888':10,'CU8888':5,'ZN8888':5,'RB8888':10,'RU8888':10,
                  'HC8888':10,'SS8888':5,'P8888':10,'J8888':100,'Y8888':10,'JM8888':60,'I8888':100,'AP8888':10,'CJ8888':5,'SR8888':10,'CF8888':5
     }
    unit = code_size[code]
    x = int(size*(10/unit))
    return str(x)
def position(code):
    pyautogui.moveTo(190,625)
    pyautogui.rightClick()
    pyautogui.press( 'down' )
    pyautogui.press( 'down' )
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    pyautogui.press( 'enter' )
    code = code.lower()
    now=datetime.datetime.now()
    now_str=now.strftime('%Y%m%d')
    name = "/root/.wine/drive_c/持仓_" + now_str[2:] + ".csv"
    time.sleep(1)
    f = open(name, 'rb').read().decode('gbk')
    if code in f:
        print("执行买卖开仓成功.")
        #x = f.split(str="\n")
        return 1
    else:
        print("执行买卖平仓成功.")
        return 0

def buy_open(code,size):
    
    time.sleep(2)
    pyautogui.moveTo(60,325)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(code, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.moveTo(53,355)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(54,378)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(91,410)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(size, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.moveTo(95,443)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(62,477)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(100,488)
    pyautogui.click()
    time.sleep(1)
    x = position(code)
    print(x)
    return x

def sell_open(code,size):
    time.sleep(1)
    pyautogui.moveTo(60,325)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(code, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.moveTo(101,356)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(54,378)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(91,410)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(size, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.moveTo(95,443)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(62,477)
    pyautogui.click()
    time.sleep(1)
    
    pyautogui.moveTo(100,488)
    pyautogui.click()
    time.sleep(1)
    
    x = position(code)
    return x
    
def sell_close(code,size):
    time.sleep(1)
    pyautogui.moveTo(60,325)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(code, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.moveTo(101,356)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(149,378)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(91,410)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(size, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.moveTo(95,443)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(62,477)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(100,488)
    pyautogui.click()
    time.sleep(1)
    
    x = position(code)
    return x

    

def buy_close(code,size):
    time.sleep(1)

    
    pyautogui.moveTo(60,325)
    pyautogui.click()
    time.sleep(1)

    pyautogui.write(code, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)

    pyautogui.moveTo(53,355)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(149,378)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(91,410)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(size, interval=0.3)
    pyautogui.press( 'enter' )
    time.sleep(1)
    pyautogui.moveTo(95,443)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(62,477)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(100,488)
    pyautogui.click()
    time.sleep(1)
    
    x = position(code)
    return x


#buy_open("I","14")
# open_close('C2109','1')
# print(x,y)
# pyautogui.moveTo(60,514,0.5)
# pyautogui.doubleClick()
# time.sleep(3)
# pyautogui.moveTo(362,82,0.5)
# pyautogui.click()
# pyautogui.click()
# pyautogui.click()
# pg.write('https://v.kuaishou.com/bU9cdS', interval=0.3)
# pyautogui . press( 'enter' )
# time.sleep(3)
# pyautogui.moveTo(906,53,0.5)
# pyautogui.moveTo(861,70,0.5)


# In[ ]:





# In[ ]:





# In[ ]:




