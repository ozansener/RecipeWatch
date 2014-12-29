import glob
import re
import os

Folds = glob.glob('*/')

fol = ''
print 'Folder:',fol
file_list = open(fol+'videos.txt','r').read()
try:
	os.mkdir('./'+fol+'Frames/')
	#os.mkdir('./'+fol+'Frames_CPMC/')
except:
	print 'Creation'

for f in file_list.split():
	print '\t Video:',f
	#Convert video into frames
	try:
		os.mkdir('./'+fol+'Frames/'+f+'/')
		#os.mkdir('./'+fol+'Frames_CPMC/'+f+'/')
	except:
		print 'Err'

	try:
		os.system('ffmpeg -i '+fol+'CleanVideos/C_'+f+'.mp4 2> '+fol+'C_'+f+'.info')
		#os.system('ffmpeg -i '+fol+'CleanVideos/C_'+f+'.mp4 -r 5 -f image2 '+fol+'Frames_CPMC/'+f+'/'+f+'%05d.png')
	except:
		print '\t \t Frame Genetation Failed'

	try:
		os.system('ffmpeg -i '+fol+'FullVideos/'+f+'.mp4 2> '+fol+f+'.info')
		os.system('ffmpeg -i '+fol+'FullVideos/'+f+'.mp4 -f image2 '+fol+'Frames/'+f+'/'+f+'%05d.png')

	except:
		print '\t \t Frame Genetation Failed'
