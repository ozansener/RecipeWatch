import scipy as sp
import numpy as np

def getArtificialProblem(NumVisObjs = 10,NumLangObjs = 15,NumVIDS = 100,NumSTs = 20,noise=0.3,plotting = False,fileName=''):
  #Sample the subtask histograms from DP
  sv = np.random.beta(0.4,0.4,[NumSTs,NumVisObjs])
  sl = np.random.beta(0.4,0.4,[NumSTs,NumLangObjs])

  #Now sample the temporal durations
  Dur =  np.random.geometric(p=0.2,size=NumSTs)

  #Sample the constraints
  SomeRN = np.random.permutation(NumSTs*NumSTs);

  NumbCoNorConst =  np.random.poisson(lam=2)
  CoNorConst = SomeRN[0:NumbCoNorConst+1]
  #print "Co-Not Occurance requirements"
  #print "\t",CoNorConst/NumSTs,CoNorConst%NumSTs

  RemainingPairs =  SomeRN[NumbCoNorConst+1:]
  NumbCoOrder =  np.random.poisson(lam=2)
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
      for z in range(Leng):
        ll=[]
        vv=[]
        for lz in range(NumLangObjs):
          if np.random.rand() >noise:
            ll.append(np.random.binomial(1,sl[ts,lz]))
          else:
            ll.append(np.random.binomial(1,0.5))
        for vz in range(NumVisObjs):
          if np.random.rand() >noise:
            vv.append(np.random.binomial(1,sv[ts,vz]))
          else:
            vv.append(np.random.binomial(1,0.5))
        VisVid=np.concatenate((VisVid,np.mat(vv)),axis=0)
        LanVid=np.concatenate((LanVid,np.mat(ll)),axis=0)
      gtTS=np.concatenate((gtTS,np.kron(np.ones((Leng,1)),ts)),axis=0)
    VidL.append((VisVid[1:,:],LanVid[1:,:],gtTS[1:,:]))
  #print 'TT:',tp
  return {'Durations':Dur,'CoNotOccur':CNCor,'CoNotOrder':CNOr,'VisualMeans':sv,'LanguageMeans':sl,'Videos':VidL,'VideoLength':vidLengths}
