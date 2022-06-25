# encoding:utf-8
import re,os
while True:
    os.system('tcpdump -n -s 0 -X -l -c 10000 -w x.cap')
    f = open("x.cap", encoding='latin-1')

    txt = f.read()
    #print(txt[3333:4444])
    res= r'(rtmp.*live/.*)'    #小狐狸直播
    res= r'](.*token=.*?)d'    #七彩直播
    url = re.findall(res,txt)

    print(url)
