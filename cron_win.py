

import pycron,time,os

while True:

    time.sleep(11)

#     if pycron.is_now('*/2 * * * *'): # True every 5 minutes

#         #print("每5分钟任务开始执行...")

# #         os.system("python C:/cc_trade.py")

#         time.sleep(1)       

    if pycron.is_now('03 * * * *'):

        print("每小时任务开始执行...")

        os.system('python C:/Download_data_60m.py') #下载期货60分钟品种数据 
        os.system('python C:/auto888_qh.py')     #每小时自动执行期货交易
        time.sleep(50)

    # 每日股票任务执行。

    if pycron.is_now('31 09 * * *'):

        print("9点31任务开始")
        os.system('python C:/auto888_1d.py')  #股票交易
        time.sleep(50)

    if pycron.is_now('31 10 * * *'):

        print('10点31任务开始')
        os.system('python C:/auto888_1d.py')   #股票交易
        time.sleep(50)

    if pycron.is_now('01 13 * * *'):

        print("13点01任务开始")

        os.system('python C:/auto888_1d.py')   #股票交易
        time.sleep(50)

    if pycron.is_now('01 14 * * *'):

        print("14点01任务开始")

        os.system('python C:/auto888_1d.py')   #股票交易
        time.sleep(50)

    if pycron.is_now('59 14 * * *'):

        print("14点59任务开始")

        os.system('python C:/auto888_1d.py')   #股票交易     
        time.sleep(50)

        
    
    
    


# In[ ]:



