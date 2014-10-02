import scipy as sp
import numpy as np
import pandas as pd
#import ggplot



def getArtificialProblem(DIM = 2,NumVisObjs = 10,NumLangObjs = 15,NumVIDS = 100,NumSTs = 20,plotting = False):
  #Sample the subtask histograms from DP
  sv = np.random.dirichlet(0.1*np.ones([NumVisObjs,]), NumSTs)
  sl = np.random.dirichlet(0.1*np.ones([NumLangObjs,]), NumSTs)

  if plotting:
    IDS = np.mat(range(0,NumSTs))
    IDS = IDS.reshape(NumSTs,1)

    spv = np.concatenate((IDS,sv),axis=1)
    spl = np.concatenate((IDS,sl),axis=1)

    DataV = pd.DataFrame(spv,columns = ['ID']+range(0,NumVisObjs))
    DataL = pd.DataFrame(spl,columns = ['ID']+range(0,NumLangObjs))

    MeltedV = pd.melt(DataV,id_vars=['ID'])
    MeltedL = pd.melt(DataL,id_vars=['ID'])
    #print Data
    pv =  ggplot.ggplot( ggplot.aes(x='variable',y='value'),data=MeltedV) +  ggplot.geom_line()  + ggplot.facet_wrap("ID")
    pl = ggplot.ggplot( ggplot.aes(x='variable',y='value'),data=MeltedL) +  ggplot.geom_line()  + ggplot.facet_wrap("ID")
    print "Saving mean histograms"
    ggplot.ggsave(pv,'visual_hists.pdf')
    ggplot.ggsave(pl,'language_hists.pdf')
    #print s[1,:]

  #Now sample the temporal durations
  Dur =  np.random.geometric(p=0.1,size=NumSTs)
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

  VidL = []
  for i in xrange(NumVIDS):
    Vid = []
    Obs = np.zeros([NumSTs,1])

    BS =np.logical_not( (CNCor*Obs+CNOr*Obs) > 0.5*np.ones([NumSTs,1]))
    maxS=np.random.randint(5,15)
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
    for ts in Vid:
      Leng = int(round(np.random.exponential(Dur[ts])))+1
      ll=np.kron(np.ones((Leng,1)),sl[ts,:])+0.3*np.random.dirichlet(0.3*np.ones([NumLangObjs,]), Leng)
      vv=np.kron(np.ones((Leng,1)),sv[ts,:])+0.3*np.random.dirichlet(0.3*np.ones([NumVisObjs,]), Leng)
      VisVid=np.concatenate((VisVid,vv),axis=0)
      LanVid=np.concatenate((LanVid,ll),axis=0)
    VidL.append((VisVid,LanVid))
    return {'Durations':Dur,'CoNotOccur':CNCor,'CoNotOrder':CNOr,'VisualMeans':sv,'LanguageMeans':sl,'Videos':VidL}
