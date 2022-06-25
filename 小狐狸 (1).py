# encoding:utf-8
#匹配网址rtmp://6s2z27kp8g3f8sofztf2.zgxhzm.com/live/80941336_f3a144c2b38b999b0f33d0efd1770cf2?token=c47c5fcd19d401c7d77da2ba553dc88e&t=1656164001
#匹配网址rtmp://pull.wzxpxb.cn/live/s1934094462_03cc280bf1?wsSecret=2a2b1bbf27778aebfcd8c912c5a8762b&wsTime=1656164948&sign=HwjazFdf4GBdwmaVzsDUfKCxllcR-x0CUTJqdrogAl6ouLooEKGbQWLRGHHlw5w1gFuF-Y60jRVr9Z9Hq1CJ9ZBF1l9NRuJ85Ll3Y_53ufkI8Pa-9bQoqh6V57E6nb_nJVVW9P13BBa7aQ9BW1PFP28tvZ6pHVxqymyYBR4L-I4

import re,os
while True:
    os.system('tcpdump -n -s 0 -X -l -c 15000 -w x.cap')
    f = open("x.cap", encoding='latin-1')

    txt = f.read()
    #print(txt[3333:4444])
    res= r'(rtmp.*live/.*)'    #小狐狸直播
    r_rtmp = r'(rtmp.*live)'
    res2= r'(\d{5,13}.*token=.*&t=\d{5,13})'    #七彩直播
    rtmp =re.findall(r_rtmp,txt)
    url = re.findall(res,txt)
    url2 =re.findall(res2,txt)
    try:
        url1 = url[0]
        url2 = rtmp[0] + "/" + url2[0]
    except:
        #url1 = "获取错误1"
        url2 = "获取错误2"
    print(url1,url2)
