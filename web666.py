from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re
import os
import time
import random

mobile_emulation ={ 
            
            "deviceName": "iPhone 6"
            
            }
 
os.system("killall chrome >/dev/null 2>&1 &") 
print("清理进程结束")
chrome_options = Options() 
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox') # 这个配置很重要
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/bin/chromedriver') 
driver.implicitly_wait(10)

def find_url(url):
	try:

		driver.get(url) 
		driver.implicitly_wait(10)
		time.sleep(7)

		driver.refresh()
		time.sleep(3)
		html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
		#print(html)

		#html= driver.page_source

		res = r'application/x-mpegURL" src="(.*?)" alt='

		url = re.findall (res,html)
		x = url[0].replace('&amp;','&')
		x = x.replace('https','http')
		os.system("echo '" + x + "' >>/data/Downloads/dizhi.txt")

		res = r'show\/(.*?).m3u8'
		flv = re.findall(res,x)
		flv = "/data/Downloads/" + flv[0] + ".mp4"
		#print("Downloads....  " + x)
		mp4 = 'nohup ffmpeg -i "' + x + '" -pix_fmt yuv420p -c copy ' +  flv + "  >/dev/null 2>&1 &"

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
			os.system(mp4)
			print("执行下载成功...")
		
		return x
	except:
		return "erro"


url2 = "https://v.kuaishou.com/7iKSOM"
url1 = 'https://klsbeijing.m.chenzhongtech.com/fw/live/3xs5wu37h6utihq?fid=123102539&cc=share_copylink&groupName=E_5_190101223657061_G_1&appType=21&docId=5&shareId=117396493622&shareToken=X7ntzmoEc5Kn_9jFTKtwTW4o1US&userId=764420205&shareType=5&et=1_a/2000018879321925090_f81sl&timestamp=1579878315581'
#url2 = 'http://m.gifshow.com/fw/live/3xqjysrhmr48uam?fid=123102539&cc=share_copylink&groupName=E_5_190101223657061_G_1&appType=21&docId=5&shareId=49191403452&shareToken=X6tcxb1gxBDA_3ZT812x5AoG1CR&userId=386882764&shareType=5&et=1_a/1641038029457219589_f81&timestamp=1565015929731'
url3 = 'https://v.kuaishou.com/8ATp8Z'
#url3 = 'https://v.kuaishou.com/fw/live/dcx-888888?fid=123102539&cc=share_copylink&appType=21&docId=5&shareId=140007880001&shareToken=X-4TSH58Yi2y1_fvsRqWNMJb1NE&userId=776325709&shareType=5&et=1_a/2000032618337729345_f108&timestamp=1584268882809'
html1 = find_url(url1)
html2 = find_url(url2)
html3 = find_url(url3)



driver.quit() 

print("地址1:" + html1)




print("地址2:" + html2)


print("地址3:" + html3)

