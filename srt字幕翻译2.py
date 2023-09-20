import re
import html
from urllib import parse
import requests
import time
import os
GOOGLE_TRANSLATE_URL = 'http://translate.google.com/m?q=%s&tl=%s&sl=%s'

def srt(name):
    with open("srt/" + name , "rb") as f:  # 打开文件
        data = f.read()  # 读取文件
    size  = len(data)
    print(size)
    for i in range(0,size,2000):
        z = i + 2000
        print(z)
        if z < size :
            txt = translate(data[i:z],"zh-CN","en")
            r = open("CN_" + name ,"a")
            r.write(txt)
            r.close()
        time.sleep(0.3)
        print(txt)
    print("翻译结束！")




def translate(text, to_language="auto", text_language="auto"):

    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text,to_language,text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""

    return html.unescape(result[0])

#print(translate("你吃饭了么?", "en","zh-CN")) #汉语转英语
#print(translate("你吃饭了么？", "ja","zh-CN")) #汉语转日语
print(translate("about your situation", "zh-CN","en")) #英语转汉语
#txt = srt("/root/1.srt")
while True:
    try:
        time.sleep(8)
        name = os.popen("ls ./srt/").read().rstrip() 
        print(name)
        srt(name)
        os.system("rm -rf ./srt/'" + name + "'")
    except:
        print("没有检测到需要翻译的1.srt文件")

