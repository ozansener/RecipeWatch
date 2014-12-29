import glob
import re
import os

Folds = glob.glob('*/Frames_CPMC_Scaled/*/')

for fol in Folds:
	print fol
	abc = re.sub('/','',re.sub('^[^/]+/Frames_CPMC_Scaled/','',fol))
	defd = re.sub('/.*','',fol)
	print 'cp -rf '+defd+'/CPMC/cpmc_base/ '+defd+'/CPMC/cpmc_'+abc+'/'
	os.system( 'cp -rf '+defd+'/CPMC/cpmc_base/ '+defd+'/CPMC/cpmc_'+abc+'/')
	print 'cp '+defd+'/Frames_CPMC_Scaled/'+abc+'/* '+defd+'/CPMC/cpmc_'+abc+'/data/JPEGImages/'
	os.system( 'cp '+defd+'/Frames_CPMC_Scaled/'+abc+'/*.jpg '+defd+'/CPMC/cpmc_'+abc+'/data/JPEGImages/')
