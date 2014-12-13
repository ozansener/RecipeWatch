from scipy.cluster.vq import vq,kmeans,whiten

import numpy as np
import scipy as sp


def ApplyKMeansToProblem(Problem,K):
  VV = Problem['Videos'][0][0]
  LN = Problem['Videos'][0][1]

  for i in xrange(1,len(Problem['Videos'])):
    VV=np.concatenate((VV,Problem['Videos'][i][0]),axis=0)
    LN=np.concatenate((LN,Problem['Videos'][i][1]),axis=0)
  Dat = np.concatenate((VV,LN),axis=1)
  wDat = whiten(Dat)
  mns_ = kmeans(Dat,K)
  mns = mns_[0]

  idS,_ = vq(wDat,mns)
  return Dat,idS
