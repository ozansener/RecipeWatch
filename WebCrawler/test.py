from Crawler.Crawler import Crawler
import re
import os
#'1QK-DGlRcTo','7-9OEohpivA','lbzhyvH74w8','qX7A0LPIuKs','s1oUDsonIzg','-sSni2HTfvM','wdasrVE5NOc',
VIDS = ['lbzhyvH74w8']
for vi in VIDS:
    print vi
    os.system('java -cp Subtitle.jar:commons-io-2.4.jar:jdom.jar Ozan https://www.youtube.com/watch?v='+vi+' '+'./'+vi+'.txt')
    #os.system('youtube-dl http://www.youtube.com/watch?v='+vi)
