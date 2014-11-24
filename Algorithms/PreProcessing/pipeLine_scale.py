import glob
import re
import os

Folds = glob.glob('*/Frames_CPMC/*/*')

for fol in Folds:
	print fol
	fol_n = re.sub('png','jpg',re.sub('Frames_CPMC','Frames_CPMC_Scaled',fol))
	print fol_n
	fold = re.sub('/[^/]*$','',fol_n)
	os.system( 'convert -resize x240 '+fol+' '+fol_n)
	print fold
	#if not os.path.exists(fold):
    	#	os.makedirs(fold)
