from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import requests,json,os,time

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

url1 = "https://v.kuaishou.com/7iKSOM"

driver.get(url1)

driver.implicitly_wait(10)
time.sleep(7)
driver.refresh()
time.sleep(3) 

c = driver.get_cookies()

driver.quit()

print(c)
cookies = {}
# 获取cookie中的name和value,转化成requests可以使用的形式
for cookie in c:
    cookies[cookie['name']] = cookie['value']

print(cookies)

js = json.dumps(cookies)   
file = open('/data/cookies.txt', 'w')  
file.write(js)  
file.close()  


'''
file = open('cookies.txt', 'r') 
js = file.read()
cookies = json.loads(js)   
print(cookies) 
file.close() 

headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 '
                          '(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
            }

response = requests.get(url='https://c.kuaishou.com/fw/live/3xfxv8ta383uic4?fid=123102539&cc=share_copylink&followRefer=151&shareMethod=TOKEN&docId=5&kpn=KUAISHOU&subBiz=LIVE_STREAM&shareId=780947059998&shareToken=X2jDKMnL6kdk27b_A&shareResourceType=LIVESTREAM_OTHER&userId=573248623&shareType=5&et=1_a%2F2000144191049156017_f80&shareMode=APP&originShareId=780947059998&appType=21&shareObjectId=X8PAYQyMfYQ&shareUrlOpened=0&timestamp=1606475433582', headers=headers, cookies=cookies)


print(response.text)


'''

