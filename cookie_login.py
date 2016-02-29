import urllib.request

headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
    'Cookie':'wordpress_9a7173693d9766b6634985f6371e6715=admin%7C1443691759%7Cs0onN3WbO0LMjQiiaRxkHdOQWUcL10rga8eCt5dmPyt%7C8a28be132acc996f90c9f69f5c21b9650e475ff07caff1f98e4bbb3f2bca0ccf; wp-settings-1=unfold%3D1%26posts_list_mode%3Dlist%26advImgDetails%3Dhide%26editor%3Dhtml%26hidetb%3D1; wp-settings-time-1=1443079284; a4317_pages=1; a4317_times=6; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_9a7173693d9766b6634985f6371e6715=admin%7C1443691759%7Cs0onN3WbO0LMjQiiaRxkHdOQWUcL10rga8eCt5dmPyt%7C1327c18ca549181b40663172950110e4ef7fc2a305870069b9c15ecad27d65d3'}
  
req = urllib.request.Request('http://exexue.com/wp-admin',headers = headers)
html = urllib.request.urlopen(req)
print(html.read(50000).decode('utf-8'))
