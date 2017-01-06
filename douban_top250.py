import urllib.request,re,sqlite3

class pachong:
    def __init__(self,url):
        self.url = url
        req = urllib.request.urlopen(self.url)
        html = req.read().decode('utf-8')
        self.html = html
        #print(html)
    def movies(self):
        res = r'<div class="item">[\s\S]*?<a href="(.*?)" class="">[\s\S]*?<span class="title">(.*?)</span>[\s\S]*?主演:([\s\S]*?)<br>[\s\S]*?<em>(.*?)</em>[\s\S]*?<span class="inq">(\S*?)</span>'
        movie = re.findall(res,self.html)
        conn = sqlite3.connect("d:\\test.db")
        cursor = conn.cursor()
        cursor.execute('create table user(id varchar(50) primary key,url varchar(50),zhuyan varchar(50),score int,brief varchar(50))')
        for i in movie:
            cursor.execute(r"insert into user values (?,?,?,?,?) ",(i[1],i[0],i[2],i[3],i[4]))
        cursor.close()
        conn.commit()
        conn.close()
        

if __name__ == '__main__':
    for i in range(0,250,25):
        url = 'http://movie.douban.com/top250?start=%d&filter=&type=' %i
        a = pachong(url)
        a.movies()
        break
