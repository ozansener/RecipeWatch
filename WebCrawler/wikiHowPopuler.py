from Crawler.Crawler import Crawler
import re
import os

f = open('first500','r')
for line in f:
    line = re.sub('\(.*\)','',line)
    line = re.sub('\\n','',line)
    q='how+to+'+'+'.join(line.split())
    c = Crawler(q.decode('utf-8'))
    VIDS= c.searchYoutube(25)
    for v in VIDS:
        cmd = 'youtube-dl http://www.youtube.com/watch?v='+v
        os.system(cmd)

