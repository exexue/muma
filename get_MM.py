import urllib.request
import re
import os 

def geturl (url):
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
    res = r'<img src=\"(http\:\/\/.*\.jpg)\"'
    imgurl = re.findall (res,html)
    return imgurl
    
listurl = geturl("http://jandan.net/ooxx/page-1000#comments")
print(listurl)
name = 0
for i in listurl:
    print (i)
    name +=1
    with open('c:\\'+i[92:-1]+'.jpg',"w") as f:
             data =urllib.request.urlopen(i)
             f.write(data.read())
           

                  
