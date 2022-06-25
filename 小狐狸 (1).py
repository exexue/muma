# encoding:utf-8
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
