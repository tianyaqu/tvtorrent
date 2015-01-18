# coding: utf8  
import urllib2  
import re  
import pymongo  
  
db = pymongo.Connection().torrent
url = 'https://eztv.it/page_%d'
find_re = re.compile(r'<tr name="hover" class="forum_header_border">.+?<td.+?/td>.+?thread_post".+?title="(.+?)\((.+?)\)".+?thread_post".+?<a href="(magnet:.+?)".+?thread_post">(.+?) ?</td>.+?</tr>', re.DOTALL)  

# 20页资源  
for i in range(0, 10):  
    u = url % (i)  
    # fake user agent,eztv will deny a urllib agent
    request = urllib2.Request(u)
    request.add_header('User-Agent', 'Wget/1.13.4 (linux-gnu)')
    html = urllib2.urlopen(request).read()  
    # 找到资源信息  
    for x in find_re.findall(html):  
        values = dict(
            name = x[0],
            size = x[1],
            url = x[2],
            time = x[3]
        )
        print 'name,\t',x[0]
        print 'url,\t',x[2]
        print 'size,\t',x[1]
        print 'time,\t',x[3]
        print '-------------------------------------'
        # 保存到数据库  
        db.apriate.save(values)  
  
print 'Done!'  
