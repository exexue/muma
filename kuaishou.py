# 获取快手直播的真实流媒体地址，默认输出最高画质

import json
import re
import requests,os,time


#html = requests.get(url=url,headers=headers,cookies=cookies,timeout=5).text

def find_url(url,cookies):
	try:
		headers = {
       		'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 '
                          '(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
     		}
		i = 0
		while i < 3 :
			try:

				html = requests.get(url=url,headers=headers,cookies=cookies,timeout=5).text
				
				break
			except requests.exceptions.RequestException:
				i += 1
		#print(html)
		res = r'(http.{20,100}?m3u8.*?)"'
		


		#html= driver.page_source

		#res = r'application/x-mpegURL" src="(.*?)" alt='
		url = re.findall (res,html)
		x = url[1].replace('&amp;','&')
		print(url)
		x = x.replace('https','http')
		os.system("echo '" + x + "' >>/data/dizhi.txt")

		res = r'(.{5,10}?).m3u8'
		flv = re.findall(res,x)
		flv = "/data/zhibo/" + flv[0] + ".mp4";
		#print("Downloads....  " + x)
		mp4 = "nohup ffmpeg -i '" + x + "' -vcodec h264  -c copy " +  flv + " && rclone copy " + flv + " gdrive2:share/share/  && rm -rf " + flv + "  >/dev/null 2>&1 &"

		print(mp4)
		if os.path.exists(flv):
		    #print("已经有下载任务..")
                    fsize = os.path.getsize(flv)
                    time.sleep(5)
                    ysize = os.path.getsize(flv)
                    #mp41 = 'nohup ffmpeg -i "' + x + '" -c copy ' + str(ysize) + flv + "  >/dev/null 2>&1 &"
                    if fsize == ysize:
                        print("下载卡死，重新下载。")
                        #os.system("killall ffmpeg")
                        #os.system("mv " + flv + " " + str(ysize) + flv)
                        os.system("mv " + flv + " " + str(random.randint(100,1000)) + name +".mp4")
                        os.system(mp4)
                    else:
                        print("已有下载")
		else:
			if "vod" in x:
				print("地址是回放精彩片段，不执行下载！")
			else:
				os.system(mp4)
				print("执行下载成功...")
		return x
	except:
		return "获取地址失败！"


file = open('/data/cookies.txt', 'r') 
js = file.read()
cookies = json.loads(js)   
print(cookies) 
file.close() 

url1 = "https://v.kuaishou.com/7iKSOM"

url2 = "https://v.kuaishou.com/9lcVPk"

url3 = 'https://v.kuaishou.com/8ATp8Z'

#url1='https://c.kuaishou.com/fw/live/3xntihy43vxvihk?fid=123102539&cc=share_copylink&followRefer=151&shareMethod=TOKEN&docId=5&kpn=KUAISHOU&subBiz=LIVE_STREAM&shareId=783679363938&shareToken=X-4Amj60uKYFdBzU_A&shareResourceType=LIVESTREAM_OTHER&userId=50602079&shareType=5&et=1_a%2F2000144437633929057_f80&shareMode=APP&originShareId=783679363938&appType=21&shareObjectId=FJCCHspSVlI&shareUrlOpened=0&timestamp=1606484211948'

html1 = find_url(url1,cookies)
html2 = find_url(url2,cookies)
html3 = find_url(url3,cookies)

print("地址1:" + html1)




print("地址2:" + html2)


print("地址3:" + html3)








