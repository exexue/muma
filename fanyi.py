#!/usr/bin/python3

#===============================================
# 通过有道词典进行post提交模拟翻译
#===============================================


import urllib.request
import urllib.parse
import re

running =True

while running:

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    neirong = input('请输入要翻译的内容：')
    date = {}
    date['type']= 'AUTO'
    date['i'] = neirong
    date['doctype'] = 'json'
    date['xmlVersion'] = '1.6'
    date['keyfrom'] = 'fanyi.web'
    date['ue'] = 'UTF-8'
    date['typoResult'] = 'true'
    date = urllib.parse.urlencode(date).encode('utf-8') 

    req = urllib.request.urlopen(url,date)
    html = req.read().decode('utf-8')
    res = r'tgt\":(.*?)\}'
    x = re.findall (res,html)
    for i in x:
        print ('翻译结果为：',i)
