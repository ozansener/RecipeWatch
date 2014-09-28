import glob
import re
import os
import pysrt
import pickle
import math


Folds = glob.glob('scaled*srtByName.bn')

WORDS = open('wordList.txt','r').read().split()

print WORDS

for fol in Folds:
	scaled_srt = pickle.load(open(fol,'rb'))
	fD =  re.sub('scaled','',re.sub('srtByName.bn','',fol))
	histS={}
	for k in scaled_srt:
		fN = int(re.sub('(./)|(.png)|'+fD,'',k))
		SSRT = scaled_srt[k].split()
		hist = [0 for x in WORDS]
		for sw in SSRT:
			for ii,ww in enumerate(WORDS):
				if ww in sw:
					hist[ii]+=1
		histS[fN]=hist
	pickle.dump(histS,open('hist_srt'+fD+'.bn','wb'))
