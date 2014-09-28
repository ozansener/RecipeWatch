import glob
import re
import os
import numpy,scipy.io

Folds = glob.glob('*/CPMC/*/data/Masks/*.mat')

MN = []
IN = []
FN = []
for fol in Folds:
	#print fol
	MN.append(fol)
	IMName =  re.sub('mat','jpg',re.sub('Masks','JPEGImages',fol))
	IN.append(IMName)
	FOLName = re.sub('/data.*','',re.sub('^[^/]+/CPMC/','',fol))
	FN.append(FOLName)
scipy.io.savemat('HIS_LIS.mat',mdict={'MAT':MN,'Image':IN,'Fols':FN})

