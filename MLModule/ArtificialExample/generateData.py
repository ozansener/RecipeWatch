import scipy as sp
import numpy as np
import pandas as pd

from Utilities import plot

def getArtificialProblem(NumVisObjs = 10,NumLangObjs = 15,NumVIDS = 100,NumSTs = 20,noise=0.3,plotting = False,fileName=''):
  #Sample the subtask histograms from DP
  sv = np.random.dirichlet(0.1*np.ones([NumVisObjs,]), NumSTs)
  sl = np.random.dirichlet(0.1*np.ones([NumLangObjs,]), NumSTs)
  if plotting:
    plot.plotHistogramMeans(np.concatenate((sv,sl),axis=1),fileName)


  #Now sample the temporal durations
  Dur =  np.random.geometric(p=0.2,size=NumSTs)
  #print "Mean durations of sub-tasks:"
  #print "\t",Dur

  #Sample the constraints ? should I start with objects or is it too much information ?
  SomeRN = np.random.permutation(NumSTs*NumSTs);

  NumbCoNorConst =  np.random.poisson(lam=6)
  CoNorConst = SomeRN[0:NumbCoNorConst+1]
  #print "Co-Not Occurance requirements"
  #print "\t",CoNorConst/NumSTs,CoNorConst%NumSTs

  RemainingPairs =  SomeRN[NumbCoNorConst+1:]
  NumbCoOrder =  np.random.poisson(lam=10)
  OrderConst = RemainingPairs[0:NumbCoOrder+1]
  #print "Co-Not Ordering requirements"
  #print "\t",OrderConst/NumSTs,OrderConst%NumSTs

  CNCor = np.matrix(np.zeros([NumSTs,NumSTs]));
  CNCor[CoNorConst/NumSTs,CoNorConst%NumSTs]=1
  CNCor[CoNorConst%NumSTs,CoNorConst/NumSTs]=1
  #print "Co-Not Occurance Matrix"
  #print CNCor

  CNOr = np.matrix(np.zeros([NumSTs,NumSTs]));
  CNOr[OrderConst/NumSTs,OrderConst%NumSTs]=1;
  #print "Co-Not Order Matrix"
  #print CNOr
  #tp = 0
  VidL = []
  vidLengths = np.zeros([NumVIDS,])
  for i in xrange(NumVIDS):
    Vid = []
    Obs = np.zeros([NumSTs,1])

    BS =np.logical_not( (CNCor*Obs+CNOr*Obs) > 0.5*np.ones([NumSTs,1]))
    maxS=np.random.randint(5,10)
    lastC = -1;
    while np.any(BS) and len(Vid)<maxS:
      k = np.random.randint(0,NumSTs)
      if BS[k,0] and not k==lastC:
        Vid.append(k)
        Obs[k,0]=1
        lastC = k
      BS =np.logical_not( (CNCor*Obs+CNOr*Obs) > 0.5*np.ones([NumSTs,1]))
    #print Vid
    #print Dur
    VisVid=np.zeros((1,NumVisObjs))
    LanVid=np.zeros((1,NumLangObjs))
    gtTS=np.zeros((1,1))
    for ts in Vid:
      Leng = int(round(np.random.exponential(Dur[ts])))+1
      vidLengths[i] = vidLengths[i] + Leng
      #tp = tp + Leng
      ll=np.kron(np.ones((Leng,1)),sl[ts,:])+noise*np.random.dirichlet(0.3*np.ones([NumLangObjs,]), Leng)
      vv=np.kron(np.ones((Leng,1)),sv[ts,:])+noise*np.random.dirichlet(0.3*np.ones([NumVisObjs,]), Leng)
      gtTS=np.concatenate((gtTS,np.kron(np.ones((Leng,1)),ts)),axis=0)
      VisVid=np.concatenate((VisVid,vv),axis=0)
      LanVid=np.concatenate((LanVid,ll),axis=0)
    VisVid = VisVid/VisVid.sum(axis=1)[:,np.newaxis]
    LanVid = LanVid/LanVid.sum(axis=1)[:,np.newaxis]
    VidL.append((VisVid[1:,:],LanVid[1:,:],gtTS[1:,:]))
  #print 'TT:',tp
  return {'Durations':Dur,'CoNotOccur':CNCor,'CoNotOrder':CNOr,'VisualMeans':sv,'LanguageMeans':sl,'Videos':VidL,'VideoLength':vidLengths}
