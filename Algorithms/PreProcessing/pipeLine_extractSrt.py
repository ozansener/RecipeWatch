import glob
import re
import os
import pysrt
import pickle
import math

def str2sec(dSI,sp1):
	dS = dSI.split(sp1);
	durN = float(str(int(dS[0].split(':')[0])*60*60+int(dS[0].split(':')[1])*60+int(dS[0].split(':')[2]))+'.'+dS[1])
	return durN

def fixNum(inp,maxim):
	if inp<1:
		return 1
	if inp>=maxim:
		return maxim-1
	return inp


fol = ''
files = glob.glob(fol+'SRT/*.srt')
for fi in files:
	print fi
	vi=re.sub('_srt.srt','',re.sub('.*/','',fi));
#		print vi+'.info'
	f = open(fol+vi+'.info','r').read()
	fps = re.search(',\s([\.\d]*)\sfps', f)
	fpsN =  float(fps.group(1))
#
	dur = re.search('Duration:\s([:\d\.]*),', f)
	durN = str2sec(dur.group(1),'.')

	im2h = pickle.load( open( fol+vi +"Im2Hash.bn", "rb" ) );

	NumF = len(im2h) - 1;
	print 'FPS:',fpsN,'Duration:',durN,'Dur*FPS:',durN*fpsN,'#Frames:',NumF + 1
	subs = pysrt.open(fi)

	subSt = {}
	for i in range(1,NumF):
		subSt[i]=''
	for sN in subs:
		FFS = int(math.floor(str2sec(str(sN.start),',')*fpsN))+1
		FLS = int(math.ceil(str2sec(str(sN.start),',')*fpsN))+1
		for j in range(fixNum(FFS-100,NumF),fixNum(FFS+100,NumF)): #Frames are 1 indexed
			subSt[j]=subSt[j]+' '+sN.text

	pickle.dump( subSt, open(fol+ vi+"srtByFrames.bn", "wb" ) )
