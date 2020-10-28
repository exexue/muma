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


url2 = "https://v.kuaishou.com/7iKSO"
url1 = 'https://klsbeijing.m.chenzhongtech.com/fw/live/3xs5wu3'
#url2 = 'http://m.gifshow.com/fw/live/3xqjysrhmr4'
url3 = 'https://v.kuaishou.com/8AT'
#url3 = 'https://v.kuaishou.com/fw/live/dcx-888'
html1 = find_url(url1)
html2 = find_url(url2)
html3 = find_url(url3)



driver.quit() 

print("地址1:" + html1)




print("地址2:" + html2)


print("地址3:" + html3)

