import numpy as np
import scipy as sp
import scipy.misc as sc

import pdb

class NPBPSampler:
  def __init__(self):
    self.c0 = 1
  def sampleEta(self):
    self.eta = [np.mat(np.zeros((self.F.shape[1],self.F.shape[1]))) for k in xrange(len(self.videos))]
    #We will sample eta for each videos
    for numV,vid in enumerate(self.videos):
    #Start with collecting the sufficient statistics
      tranMat = np.ones((self.F.shape[1],self.F.shape[1]))*self.lamb
      tranMat[np.diag_indices(self.F.shape[1])]=self.kappa
      for i in range(len(vid)-1):
        tranMat[vid[i]['state'],vid[i+1]['state']] = tranMat[vid[i]['state'],vid[i+1]['state']] + 1

      #Get only the selected features
      i,j=self.F[numV,:].nonzero()
      selFeats = np.array(j).reshape(-1,).tolist()

      for st in range(self.F.shape[1]):
        if self.F[numV,st]==1:
          self.eta[numV][st,:]=np.mat(np.zeros((1,self.F.shape[1])))
          self.eta[numV][st,selFeats]=np.random.dirichlet( tranMat[st,selFeats])*np.random.gamma(self.lamb*len(selFeats)+self.kappa)
        else:
          self.eta[numV][st,:]=np.mat(np.zeros((1,self.F.shape[1])))
      #print self.eta[numV],np.random.gamma(self.lamb*len(selFeats)+self.kappa)
    return 0


  def sampleTheta(self):
    #1st sample visual occurances
    self.states['v']=[np.mat(np.zeros((self.F.shape[1],self.numVidObjs)))]
    self.states['l']=[np.mat(np.zeros((self.F.shape[1],self.numLangObjs)))]
    #Collect the sufficient statistics
    countStates = np.mat(np.zeros(self.F.shape[1]))
    countVStatistics = np.mat(np.zeros((self.F.shape[1],self.numVidObjs)))
    countLStatistics = np.mat(np.zeros((self.F.shape[1],self.numLangObjs)))
    for vid in self.videos:
      for frame in vid:
        countStates[0,frame['state']]+=1
        countVStatistics[frame['state'],:]+=frame['obsV']
        countLStatistics[frame['state'],:]+=frame['obsL']
    #Sample the beta varaible
    for k in range(self.F.shape[1]):
      for j in  range(self.numVidObjs):
        self.states['v'][0][k,j]=np.random.beta(self.alpha0+countVStatistics[k,j],self.beta0+(countStates[k]-countVStatistics[k,j]),1)[0]
        #self.states['v'][k][j][1]=np.random.dirichlet(alphaFlow+histStatistics[k,j,:])

    #2nd sample language occurances
    for k in range(self.F.shape[1]):
      for j in range(self.numLangObjs):
        self.states['l'][0][k,j]=np.random.beta(self.alpha0+countLStatistics[k,j],self.beta0+(countStates[k]-countLStatistics[k,j]),1)[0]
    #print self.states['v']
    #print self.states['l']
  def solveFactorization(self):
    return 0
  def sampleCoMatrices(self):
    return 0
  def sampleStates(self):
    return 0
  def sampleBPHyperParams(self):
    return 0
  def sampleHMMHyperParams(self):
    return 0
  def sampleUniqueFeatures(self):
    return 0
  def sampleSharedFeatures(self):
    return 0
  def calcLogProbF(self):
    # P(F|\gamma,\alpha)
    # Compute probability of observed feature assignment matrix as function of the 2-parameter Indian Buffet Process  using the hyperparams  gamma (mass) and c0 (conc)
    # see eq. 21 of Ghahramani, Griffiths, and Sollich  "Bayesian nonparametric latent feature models" ISBA 8th World Meeting on Bayesian Statistics, 2006

    #Choose only the used features
    #pdb.set_trace()
    (i,j)=np.sum(self.F,0).nonzero()
    FDummy = self.F[:,np.asarray(j)[0]]
    (N,K)=FDummy.shape
    M=np.sum(FDummy,0)
    #Get the unique columns, looks ugly but it basically use set structure of python to find uniques
    UniqueF = np.vstack(set(map(tuple,np.asarray(FDummy.T))))
    nU = UniqueF.shape[0]

    logKh = 0
    for nn in range(nU):
      logKh = logKh+ sp.special.gammaln(map(tuple,np.asarray(FDummy.T)).count(tuple(UniqueF[nn,:]))+1)


    logProdFactors = 0
    for k in range(K):
      logProdFactors = logProdFactors + sp.special.betaln( M[k,0], N-M[k,0] + self.c0 )

    Harmonic_N = np.sum(self.c0 / ( self.c0 -1 + np.array(range(1,N+1))))

    return  K*np.log( self.gamma ) + K*np.log(self.c0) - logKh - self.gamma*Harmonic_N  +  logProdFactors

  def calcLogProbZgivenF(self):
    #Compute p(Z|F), it is a dirichelet distribution
    #Compute the sufficient statistics through counting
    tranMat = np.ones((self.F.shape[1],self.F.shape[1]))*self.lamb
    tranMat[np.diag_indices(self.F.shape[1])]=self.kappa
    priorProb = np.sum(sp.special.gammaln(tranMat)) - np.sum(sp.special.gammaln(np.sum(tranMat,1)))

    for vid in self.videos:
      for i in range(len(vid)-1):
        tranMat[vid[i]['state'],vid[i+1]['state']] = tranMat[vid[i]['state'],vid[i+1]['state']] + 1
    #Now compute the likelihood
    return np.sum(sp.special.gammaln(tranMat)) - np.sum(sp.special.gammaln(np.sum(tranMat,1))) - priorProb

  def calcLogProbObsgivenFZ(self):
    #Compute P(X|Z,F), it is a beta distribution
    countVid = np.zeros(self.numVidObjs)
    countLang = np.zeros(self.numLangObjs)
    genCNT = 0
    for vid in self.videos:
      genCNT = genCNT+len(vid)
      for frame in vid:
        countVid=countVid+frame['obsV']
        countLang=countLang+frame['obsL']
    obsProb = sum([sp.special.betaln(self.alpha0+countVid[0,i],self.beta0+genCNT-countVid[0,i]) for i in range(self.numVidObjs)])
    obsProb = obsProb + sum([sp.special.betaln(self.alpha0+countLang[0,i],self.beta0+genCNT-countLang[0,i]) for i in range(self.numLangObjs)])
    return obsProb-sp.special.betaln(self.alpha0,self.beta0)

  def sampleNextState(self):
    #self.sampleSharedFeats()
    #self.sampleUniqueFeats()
    #self.sampleStateSeq()
    self.sampleEta()
    self.sampleTheta()

    return 0

  def runBPRecipe(self,problemInstance):
    #initialize
    self.F = np.mat(np.ones((len(problemInstance['Videos']),1))) # All videos are from a single mean
    #self.F = np.mat(np.ones((5,1))) # All videos are from a single mean
    self.c0 = 1.0
    self.gamma = 2.0
    self.alpha0 = 0.7
    self.beta0 = 0.7
    self.nIter = 10
    self.lamb = 1.0
    self.kappa = 25.0
    self.numVidObjs = 10
    self.numLangObjs = 15
    self.states = {}
    self.videos = [[{'state':0,'obsV':V[0][i,:],'obsL':V[1][i,:]} for i in range(V[0].shape[0])] for V in problemInstance['Videos']]
    # Compute the probability of F
    for n in range(self.nIter):
      self.sampleNextState()
      exceptProb = self.calcLogProbF() + self.calcLogProbZgivenF()
      currentProb = exceptProb + self.calcLogProbObsgivenFZ()
      print 'Iteration #%d Log-ProbabilityF,Z: %f Log-Probability Total:%f' %(n,exceptProb,currentProb)
    return 0
