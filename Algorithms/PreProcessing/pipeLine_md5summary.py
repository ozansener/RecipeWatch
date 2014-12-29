import glob
import re
import os
import hashlib
import pickle
from PIL import Image


fol = ''
print 'Folder:',fol
file_list = open(fol+'videos.txt','r').read()
print file_list
for f in file_list.split():
	FrameList = glob.glob('./'+fol+'Frames/'+f+'/*.png');
	hash2im = {}
	im2hash = {}
	for fr in FrameList:
		jpgfile = Image.open(fr)
		has = hashlib.md5(str(list(jpgfile.getdata()))).hexdigest()
		im = re.sub(fol+'Frames/'+f+'/','',fr)
		hash2im[has]=im
		im2hash[im]=has
	fih = open('./'+fol+f+'Im2Hash.bn','wb')
	fhi = open('./'+fol+f+'Hash2Im.bn','wb')
	pickle.dump(im2hash,fih)
	pickle.dump(hash2im,fhi)


	SFrameList = glob.glob('./'+fol+'Frames_CPMC/'+f+'/*.png');
	im2hash = {}
	for fr in SFrameList:
		jpgfile = Image.open(fr)
		has = hashlib.md5(str(list(jpgfile.getdata()))).hexdigest()
		im = re.sub(fol+'Frames_CPMC/'+f+'/','',fr)
		im2hash[im]=has
	fih = open('./'+fol+'scaled'+f+'Im2Hash.bn','wb')
	pickle.dump(im2hash,fih)
