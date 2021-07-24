#!/usr/bin/env python
# coding: utf-8

# In[21]:


import datetime,os,pycron
import pandas as pd
import time as tm
from jqdatasdk import *
auth('****','****') 
count=get_query_count()
print(count)

def to_data(dt,code,time):
    data = pd.read_csv("./data/" + time  +"/" + code)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index("date",inplace=True)
    x = str(dt.index.tolist()[0])
    print(x)
    data = data.loc[:x] 
    
    data = data.append(dt[1:])
    data.to_csv("./data/" + time + "/" + code )
    print("追加数据完成")


def to_csv(code,time):
    code =normalize_code(code)
    print(code)
    #最少获取数据3行
    data = get_bars(code,count=3, unit=time,fields=['date','open','high','low','close'],include_now=True,end_dt=datetime.datetime.now(),fq_ref_date =None)
    print(data)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index("date",inplace=True)
    #data.to_csv("/code/data/" + time + "/" + code)
    to_data(data,code,time)
    tm.sleep(1)
    
if __name__ == '__main__':
    code_range =['JD8888','BU8888','UR8888','C8888','M8888','RM8888','TA8888','MA8888','FG8888','PF8888','SA8888','FU8888',
                 'CU8888','AG8888','AL8888','ZN8888','RB8888','RU8888','HC8888','SS8888','P8888','J8888','Y8888','JM8888','I8888','AP8888','CJ8888',
                 'SR8888','CF8888']
    #code_range =['C8888','M8888']
    #code_range = ["AG8888"]
    
    for code_name in code_range:
        to_csv(code_name,'60m')  #'1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w'(一周), '1M'（一月）
        #print(code_name)
    
    
#     while True:
#         tm.sleep(10)
#         if pycron.is_now('03 * * * *'):
#             print("每小时任务开始执行...")
#             for code_name in code_range:
#                 to_csv(code_name,'60m')  #'1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w'(一周), '1M'（一月）
#                 #print(code_name)
#             os.system("python C:/auto888_qh.py")
#             tm.sleep(50)
        
        





