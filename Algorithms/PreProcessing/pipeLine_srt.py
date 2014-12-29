import glob
import re
import os

Folds = glob.glob('*/')

for fol in Folds:
	print 'Folder:',fol
	file_list = open(fol+'videos.txt','r').read()
	for f in file_list.split():
		print '\t Video:',f
		#Download the Subtitles if they exist
		try:
			os.system('java -cp Subtitle.jar:commons-io-2.4.jar:jdom.jar Ozan https://www.youtube.com/watch?v='+f+' '+'./'+fol+'SRT/'+f+'_srt.txt')
		except:
			print '\t \t SRT Download Failed'
