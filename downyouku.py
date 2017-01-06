import urllib.request
import re

#获取网页源码
def gethtml(url):
    req = urllib.request.urlopen(url)
    html = req.read().decode('utf-8')
    return html
#获取电影类型
def leixing(html):
    res = r'<li><a\s*?href="(http://www\.youku\.com/v_olist/c_96_s_1_d_1_g_.*?\.html)">(.*?)</a></li>'
    list_1 = re.findall(res,html)
    return list_1
#获取电影列表的页数
def yeshu(url):
    res = r'\.\.\.</span></li>\s*?<li><a href="(.*?)" charset=".*?">(.*?)</a></li>'
    yeshu_1 = re.findall(res,html)
    #print(yeshu_1)
    yeshu_2 = yeshu_1[0][0]
    page = yeshu_1[0][1]
    x = yeshu_2.find('p_')
    #print (page)
    url_1 = 'http://www.youku.com' + yeshu_2[0:x]
    #print(url)
    return url_1,page
def movies(html):
    res = r'<div class="p-thumb">\s*?<img src="(.*?)" alt="(.*?)">[\s\S]*?target="_blank">(.*?)</a>[\s\S]*?<span class="p-num">(.*?)</span>'
    movie_1 = re.findall(res,html)
    #print(movie_1)
    f = open('d://1.txt','a+')
    for i in movie_1:
        img = i[0]
        title = i[1]
        zhuyan = i[2]
        cishu = i[3]
        f.write(title+','+ zhuyan + ',' + cishu + ',' + img+'\n')
    f.close    



if __name__ == ('__main__'):
    html = gethtml('http://www.youku.com/v_olist/c_96.html')
    #print(html)
    leixing_list = leixing(html)
    for i in leixing_list:
        url = i[0]
        page_url,page = yeshu(url)
        for i in range(1,int(page)+1):
            new_url = page_url + 'p_%d.html' % i
            #print (new_url)
            html = gethtml(new_url)
            movies(html)
            break
        break

        
