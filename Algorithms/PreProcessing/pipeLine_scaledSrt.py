import glob
import re
import os
import pysrt
import pickle
import math


Folds = glob.glob('*/')

for fol in Folds:
	print 'Folder:',fol
	files = glob.glob(fol+'*srtByFrames.bn')
	for fi in files:
		print fi
                fN = re.sub(fol,'',re.sub('srtByFrames.bn','',fi))
		SRT_O = pickle.load(open(fi,'rb'))
		H2I = pickle.load(open(fol+fN+'Hash2Im.bn','rb'))
		SI2H = pickle.load(open(fol+'scaled'+fN+'Im2Hash.bn','rb'))
		scaled_srt = {}
		for k in SI2H:
			hs = SI2H[k]
			if hs in H2I:
				IR = H2I[hs]
				scaled_srt[k] = SRT_O[int(re.sub('./'+fN,'',re.sub('.png','',IR)))]
			else:
				print("NO"),
			#print IR
		pickle.dump(scaled_srt,open('scaled'+fN+'srtByName.bn','wb'))	
