from scipy.io import loadmat, savemat
from scipy.misc import imread, imsave
import cPickle
import subprocess
import re
import glob

from Crawler import *
from ModalDB import *
from Settings import Settings

#Crawl videos
if True:
  c = Crawler()
  q='how+to+hard+boil+an+egg'
  VIDS = c.searchYoutube(q.decode('utf-8'),5)
  print VIDS
  print 'Dowload Them'
  c.downloadVideos()
  c.getSubtitles()
  with open('ids.bn', 'wb') as fp:
    cPickle.dump(VIDS, fp)

#VIDS = cPickle.load(open('ids.bn','rb'))

import os
modaldb_client = ModalClient(root=Settings.data_dir, schema=Settings.my_schema) # here, we specify the DB's location (on disk) and schema.
#modaldb_client.clear_db() # empty the database just in case.

#Pushing videos
for vid_id in VIDS:
  title = subprocess.check_output('youtube-dl --get-filename "http://youtube.com/watch?v='+vid_id+'" -o "%(title)s"',shell=True)
  FPS=re.sub('\n','',subprocess.check_output('ffmpeg -i '+vid_id+'.mp4 2>&1 | sed -n "s/.*, \\(.*\\) fp.*/\\1/p"',shell=True))
  if os.path.exists(vid_id+'.srt'):
    subtitle_file = vid_id+'.srt'
  else:
    subtitle_file = ''

  thumb_loc=subprocess.check_output('youtube-dl --get-thumbnail "http://youtube.com/watch?v='+vid_id+'"',shell=True)
  fN = re.compile('([^/]+)\\n$').search(thumb_loc).group(1)
  os.system('wget '+thumb_loc)
  os.system('convert -resize 320 '+fN+' thumb.png')
  os.system('rm -f '+fN)
  if not subtitle_file == '':
    item_dict = {
        'thumbnail':'thumb.png',
        'title':title,
        'FPS':FPS,
        'subtitle_file':subtitle_file
    }
  else:
    item_dict = {
    'thumbnail':'thumb.png',
    'title':title,
    'FPS':FPS,
    }

  modaldb_client.insert(Video, vid_id, item_dict, method='cp')

for vid_id in VIDS:
  video = modaldb_client.get(Video, vid_id)
  os.system('mkdir '+vid_id)
  os.system('ffmpeg -i '+vid_id+'.mp4 -r 5 -f image2 '+vid_id+'/'+vid_id+'%05d.png')
  Frames = glob.glob(vid_id+'/*.png')
  for fN,frame in enumerate(Frames):
    frame0_data =  {  'image':frame,'image_scaled':re.sub('png','jpg',frame)} #This is weird requirement of CPMC, it only accepts jpg
    os.system( 'convert -resize x240 '+frame+' '+re.sub('png','jpg',frame))
    modaldb_client.insert(Frame, 'frame'+str(fN), frame0_data, parent=video, method='cp')
