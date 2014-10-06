import numpy as np
import scipy as sp
import sys
import pickle

from scipy.cluster.vq import vq,kmeans,whiten

from ArtificialExample import generateData
from Utilities import score,plot

CR = '\033[91m'
CG = '\033[92m'
CEN = '\033[00m'

def ApplyKMeansToProblem(Problem,K,Plotit=False,FileName=''):
  VV = Problem['Videos'][0][0]
  LN = Problem['Videos'][0][1]
  GT = Problem['Videos'][0][2]

  for i in xrange(1,len(Problem['Videos'])):
    VV=np.concatenate((VV,Problem['Videos'][i][0]),axis=0)
    LN=np.concatenate((LN,Problem['Videos'][i][1]),axis=0)
    GT=np.concatenate((GT,Problem['Videos'][i][2]),axis=0)
  Dat = np.concatenate((VV,LN),axis=1)
  wDat = whiten(Dat)
  mns_ = kmeans(Dat,K)
  mns = mns_[0]

  if Plotit:
    plot.plotHistogramMeans(mns,FileName)

  idS,_ = vq(wDat,mns)
  if Plotit:
    plot.saveAverageVideo(idS,mns,Problem['Videos'],FileName)
  return Dat,GT,idS


def main(argv):
  min_iou_kmeans = np.zeros((100,1))
  min_iou_kmeans_w = np.zeros((100,1))
  min_iou_oc = np.zeros((100,1))
  min_iou_rand = np.zeros((100,1))

  for (i,er) in enumerate(np.linspace(0,10,100)):
    print 'STEP:',i,er
    ProblemN = generateData.getArtificialProblem(10,15,100,20,er,False,'gt_withNoise.pdf');
    Dat,GT,idS = ApplyKMeansToProblem(ProblemN,20,False,'withNoise.pdf')
    sc = score.getMinIou(GT,idS,ProblemN['VideoLength'])

    Dat,GT,idS = ApplyKMeansToProblem(ProblemN,12,False,'withNoise.pdf')
    sc_w = score.getMinIou(GT,idS,ProblemN['VideoLength'])


    #print CG+ 'K-means IOU Score with noise(0.3):'+str(sc) + CEN
    idS,_ = vq(Dat,np.concatenate((ProblemN['VisualMeans'],ProblemN['LanguageMeans']),axis=1))
    o_sc = score.getMinIou(GT,idS,ProblemN['VideoLength'])
    #print CG+ 'Oracle Score with noise(0.3):'+str()+CEN
    r_sc = score.getMinIou(GT,np.random.randint(0,19,size=len(GT[:,0])),ProblemN['VideoLength'])
    #print CG+ 'Random IOU Score:'+str(r_sc)+CEN
    min_iou_kmeans[i,0]=sc
    min_iou_kmeans_w[i,0]=sc_w
    min_iou_oc[i,0]=o_sc
    min_iou_rand[i,0]=r_sc
  plot.plotSetOfArrays((min_iou_kmeans,min_iou_kmeans_w,min_iou_oc,min_iou_rand),['K-Means w/ Correct K','K-Means','Vector Quant','Random'],'error.png')

if __name__ == "__main__":
  main(sys.argv[1:])
