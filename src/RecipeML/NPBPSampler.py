import numpy as np
import scipy as sp
import scipy.misc as sc
import random
import time

import thread

import pdb

from Hmm import HMM
from HmmFast import HMMFast

class NPBPSampler:
  def __init__(self):
    self.c0 = 1
  def sampleEta(self):
    #self.eta = [np.mat(np.zeros((self.F.shape[1],self.F.shape[1]))) for k in xrange(len(self.videos))]
    #We will sample eta for each videos
    for numV,vid in enumerate(self.videos):
    #Start with collecting the sufficient statistics
      tranMat = np.ones((self.F.shape[1],self.F.shape[1]))*self.lamb
      tranMat[np.diag_indices(self.F.shape[1])]=self.kappa+self.lamb
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

  def mlEta(self,sq,F):
    etaP = np.mat(np.zeros((F.shape[1],F.shape[1])))
    #Start with collecting the sufficient statistics
    tranMat = np.ones((F.shape[1],F.shape[1]))*self.lamb
    tranMat[np.diag_indices(F.shape[1])]=self.kappa+self.lamb
    for vid in self.videos:
    #vid = self.videos[sq]
      for i in range(len(vid)-1):
        if vid[i]['state']>=F.shape[1] or vid[i+1]['state']>=F.shape[1]:
          continue
        tranMat[vid[i]['state'],vid[i+1]['state']] = tranMat[vid[i]['state'],vid[i+1]['state']] + 1

    #Get only the selected features
    i,j=F[sq,:].nonzero()
    selFeats = np.array(j).reshape(-1,).tolist()

    for st in range(F.shape[1]):
      if F[sq,st]==1:
        etaP[st,:]=np.mat(np.zeros((1,F.shape[1])))
        etaP[st,selFeats]=tranMat[st,selFeats]/np.sum(tranMat[st,selFeats])
      else:
        etaP[st,:]=np.mat(np.zeros((1,F.shape[1])))
    #print self.eta[numV],np.random.gamma(self.lamb*len(selFeats)+self.kappa)
    return etaP

  def mlTheta(self,sq,startW,stopW,F,newOne):
    #1st sample visual occurances
    propStates={}
    propStates['v']=[np.mat(np.zeros((F.shape[1],self.numVidObjs)))]
    propStates['l']=[np.mat(np.zeros((F.shape[1],self.numLangObjs)))]
    #Collect the sufficient statistics
    countStates = np.mat(np.zeros(F.shape[1]))
    countVStatistics = np.mat(np.zeros((F.shape[1],self.numVidObjs)))
    countLStatistics = np.mat(np.zeros((F.shape[1],self.numLangObjs)))
    for vid in self.videos:
      for frame in vid:
        if frame['state']>=F.shape[1]:
          continue
        countStates[0,frame['state']]+=1
        countVStatistics[frame['state'],:]+=frame['obsV']
        countLStatistics[frame['state'],:]+=frame['obsL']

    if not newOne == -1:
      vid = self.videos[sq]
      for k in range(startW,stopW+1):
        frame=vid[k]
        countStates[0,newOne]+=1
        countVStatistics[newOne,:]+=frame['obsV']
        countLStatistics[newOne,:]+=frame['obsL']

    #Sample the beta varaible
    for k in range(F.shape[1]):
      for j in  range(self.numVidObjs):
        propStates['v'][0][k,j]=(self.alpha0+countVStatistics[k,j])/(self.alpha0+self.beta0+countStates[0,k])

    #2nd sample language occurances
    for k in range(F.shape[1]):
      for j in range(self.numLangObjs):
        propStates['l'][0][k,j]=(self.alpha0+countLStatistics[k,j])/(self.alpha0+self.beta0+countStates[0,k])

    return propStates

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
        self.states['v'][0][k,j]=np.random.beta(self.alpha0+countVStatistics[k,j],self.beta0+(countStates[0,k]-countVStatistics[k,j]),1)[0]
        #self.states['v'][k][j][1]=np.random.dirichlet(alphaFlow+histStatistics[k,j,:])

    #2nd sample language occurances
    for k in range(self.F.shape[1]):
      for j in range(self.numLangObjs):
        self.states['l'][0][k,j]=np.random.beta(self.alpha0+countLStatistics[k,j],self.beta0+(countStates[0,k]-countLStatistics[k,j]),1)[0]

  def sampleStateSeq(self):
    for vi in range(len(self.videos)):
      self.sampleHMMStates(vi)
    return 0

  def sampleHMMStates(self,sq):
    dimension = self.eta[sq].shape[0]
    tP = np.mat(np.zeros((dimension,dimension)))
    for k in range(dimension):
      if np.sum(self.eta[sq][k,:],1)>0:
        tP[k,:]=self.eta[sq][k,:]/float(np.sum(self.eta[sq][k,:],1))
    #seq1 = HMM(dimension)
    seq2 = HMMFast(dimension)
    op= lambda x,y: (y['obsV'][0]*self.states['v'][0][x,0] + (1-y['obsV'][0])*(1-self.states['v'][0][x,0]))*(y['obsV'][1]*self.states['v'][0][x,1] + (1-y['obsV'][1])*(1-self.states['v'][0][x,1]))*(y['obsL'][0]*self.states['l'][0][x,0] + (1-y['obsL'][0])*(1-self.states['l'][0][x,0]))*(y['obsL'][1]*self.states['l'][0][x,1] + (1-y['obsL'][1])*(1-self.states['l'][0][x,1]))
    pi0 = np.mat(np.ones((dimension,1)))/float(dimension)
    #print 'KKK',tP,pi0,dimension,self.states
    seq2.setProblem(np.zeros((dimension,dimension)),np.zeros((dimension,dimension)),tP,pi0,len(self.videos[sq]),self.videos[sq],op)
    POST =  seq2.getSample()
    for t in range(len(self.videos[sq])):
      self.videos[sq][t]['state']=POST[t]

    return POST

  def getHMMObsLogProbApprox(self,seqId,tranP,statesP):
    #Write this
    dimension = tranP.shape[0]
    tP = np.mat(np.zeros((dimension,dimension)))
    for k in range(dimension):
      if np.sum(tranP[k,:],1)>0:
        tP[k,:]=tranP[k,:]/float(np.sum(tranP[k,:],1))
    #seq1 = HMM(dimension)
    seq2 = HMMFast(dimension)

    op= lambda x,y: (y['obsV'][0]*statesP['v'][0][x,0] + (1-y['obsV'][0])*(1-statesP['v'][0][x,0]))*(y['obsV'][1]*statesP['v'][0][x,1] + (1-y['obsV'][1])*(1-statesP['v'][0][x,1]))
    pi0 = np.mat(np.ones((dimension,1)))/float(dimension)

    seq2.setProblem(np.zeros((dimension,dimension)),np.zeros((dimension,dimension)),tP,pi0,len(self.videos[seqId]),self.videos[seqId],op)
    POST =  seq2.GetProbApprox()

    logP = 0
    pstG = 0
    for t in range(len(self.videos[seqId])):
      pst=0
      for k in range(dimension):
        pst+=POST[k,t]*op(k,self.videos[seqId][t])
      pstG += np.log(pst)
    #print pstG
    #print 'TP',tP,pi0,pstG
    return pstG

  def getHMMObsLogProb(self,seqId,tranP,statesP):
    #Write this
    dimension = tranP.shape[0]
    tP = np.mat(np.zeros((dimension,dimension)))
    for k in range(dimension):
      if np.sum(tranP[k,:],1)>0:
        tP[k,:]=tranP[k,:]/float(np.sum(tranP[k,:],1))
    #seq1 = HMM(dimension)
    seq2 = HMMFast(dimension)

    op= lambda x,y: (y['obsV'][0]*statesP['v'][0][x,0] + (1-y['obsV'][0])*(1-statesP['v'][0][x,0]))*(y['obsV'][1]*statesP['v'][0][x,1] + (1-y['obsV'][1])*(1-statesP['v'][0][x,1]))
    #*(y['obsL'][1]*self.states['l'][0][x,1] + (1-y['obsL'][1])*(1-self.states['v'][0][x,1]))*(y['obsL'][0]*self.states['l'][0][x,0] + (1-y['obsL'][0])*(1-self.states['l'][0][x,0]))
    pi0 = np.mat(np.ones((dimension,1)))/float(dimension)


    seq2.setProblem(np.zeros((dimension,dimension)),np.zeros((dimension,dimension)),tP,pi0,len(self.videos[seqId]),self.videos[seqId],op)
    #ts2 = time.time()
    seq2.runSmoothing()
    #te2 = time.time()
    POST =  seq2.getPosterior()
    #print 'AHA:',np.sum(POST-POST2),te-ts,te2-ts2

    logP = 0
    pstG = 0
    for t in range(len(self.videos[seqId])):
      pst=0
      for k in range(dimension):
        pst+=POST[k,t]*op(k,self.videos[seqId][t])
      pstG += np.log(pst)
    #print pstG
    #print 'TP',tP,pi0,pstG
    return pstG
  def getHMMObsProb(self,seqId,tranP,flipFt=-1):
    #Write this
    return 0.1
  def sampleUniqueFeatures(self):
    #For each video
    (N,K) = self.F.shape
    for sq in range(N):
      (N,K) = self.F.shape
      featCount = np.sum(self.F,axis=0)
      vidCount = np.sum(self.F,axis=1)
      uniqueL=[]
      for kk in range(K):
        if featCount[0,kk]==1 and self.F[sq,kk]==1:
          uniqueL.append(kk)
      #print 'A',self.F,sq,uniqueL
      #return
      if (len(uniqueL)==0 or np.random.rand()>0.6) and (K<80):
        #Birth
        #First choose data driven window length
        vid = self.videos[sq]
        if self.minW < len(vid):
          leng = int(np.random.uniform(self.minW,min(self.maxW,len(vid)-1)))
        else:
          leng = int(np.random.uniform(1,min(self.maxW,len(vid)-1)))
        startP = int(np.random.uniform(0,len(vid)-leng-1))
        EtaOld  = self.mlEta(sq,self.F)
        ThetaOld = self.mlTheta(sq,0,0,self.F,-1)

        oldProb = self.getHMMObsLogProb(sq,EtaOld,ThetaOld)

        F = np.concatenate((self.F,np.zeros((self.F.shape[0],1))),axis=1)
        F[sq,self.F.shape[1]]=1
        EtaNew  = self.mlEta(sq,F)
        ThetaNew = self.mlTheta(sq,startP,startP+leng+1,F,self.F.shape[1])


        newProb  = self.getHMMObsLogProb(sq,EtaNew,ThetaNew)
        etaa = self.gamma *1.0/(1.0 + 5.0 -1.0 );
        logPrNumFeat_Diff = ( 1 )*np.log( etaa ) +  sp.special.gammaln( F.shape[1] ) - sp.special.gammaln( F.shape[1] + 1 );
        if newProb - oldProb + logPrNumFeat_Diff > np.log(min(np.random.rand()+0.1,1)):
          self.F = F
          #self.eta[sq]=EtaNew

          #self.states = ThetaNew
          #print self.states['v'][0].shape,ThetaNew['v'][0][-1,:].shape
          self.states['v'][0]=np.concatenate((self.states['v'][0],ThetaNew['v'][0][-1,:]),axis=0)
          self.states['l'][0]=np.concatenate((self.states['l'][0],ThetaNew['v'][0][-1,:]),axis=0)

          self.eta[sq]=np.concatenate((self.eta[sq],EtaNew[:-1,-1]),axis=1)
          self.eta[sq]=np.concatenate((self.eta[sq],EtaNew[-1,:]),axis=0)

          #Update the next ones
          L1 =range(len(self.videos))
          L1.remove(sq)
          for vi in L1:
            self.eta[vi]=np.concatenate((self.eta[vi],np.zeros((self.eta[vi].shape[0],1))),axis=1)
            self.eta[vi]=np.concatenate((self.eta[vi],np.zeros((1,self.eta[vi].shape[1]))),axis=0)
          #print 'SPB',self.F.shape[1],self.states
          #update eta,theta
          return
      elif ( len(uniqueL) >0 ) and (vidCount[sq,0]>1):
        #Death
        feat2kill = np.random.choice(uniqueL)
        EtaOld  = self.mlEta(sq,self.F)
        ThetaOld = self.mlTheta(sq,0,0,self.F,-1)
        oldProb = self.getHMMObsLogProb(sq,EtaOld,ThetaOld)

        F = self.F[:,range(0,feat2kill)+range(feat2kill+1,self.F.shape[1])]
        #ThetaNew =
        EtaNew  = self.mlEta(sq,F)
        ThetaNew = self.mlTheta(sq,0,0,F,-1)
        newProb  = self.getHMMObsLogProb(sq,EtaNew,ThetaNew)

        etaa = self.gamma *1.0/(1.0 + 5.0 -1.0 );
        logPrNumFeat_Diff = ( -1.0 )*np.log( etaa ) +  sp.special.gammaln( F.shape[1]+2 ) - sp.special.gammaln( F.shape[1] + 1 );

        if newProb - oldProb + logPrNumFeat_Diff> np.log(np.random.rand()):
          #accept
          self.F = F
          #self.eta[sq]=EtaNew

          self.states['v'][0]=np.delete(self.states['v'][0],feat2kill,0)
          self.states['l'][0]=np.delete(self.states['l'][0],feat2kill,0)

          #Update the next ones
          L1 =range(len(self.videos))
          #L1.remove(sq)
          for vi in L1:
            for xx in range(feat2kill+1,self.eta[vi].shape[1]):
              for yy in range(feat2kill+1,self.eta[vi].shape[1]):
                self.eta[vi][xx-1,yy-1]=self.eta[vi][xx,yy]

            dim2kill = self.eta[vi].shape[1]-1
            self.eta[vi]=np.delete(self.eta[vi],dim2kill,1)
            self.eta[vi]=np.delete(self.eta[vi],dim2kill,0)
          #print 'SPD',self.F.shape[1],self.states
          #update eta,theta
          return
    #print 'Final',self.F.shape[1]
    return 0
  def sampleSharedFeats(self):
    #We only sample the columns who has more than one video to support it. In other words, we do not sample features unqiue to a specific video.
    #First compute the number of occurences of each feature
    featCount = np.sum(self.F,axis=0)
    vidCount = np.sum(self.F,axis=1)
    (N,K) = self.F.shape
    for sq in range(N):
      #First sample transition probabilities
      priorEt = np.mat(np.zeros((K,K)))
      ppPI = np.mat(np.zeros((K,K)))

      for st in range(K):
        pr = np.ones(K)*self.lamb
        pr[st] = self.lamb+ self.kappa
        priorEt[st,:] = np.random.dirichlet(pr,1)*np.random.gamma(self.lamb+self.kappa)#self.eta[sq][st,:]#2 #
        for stt in range(K):
          if (self.F[sq,st]==1) and (self.F[sq,stt]==1):
            priorEt[st,stt]=self.eta[sq][st,stt]
            ppPI[st,stt]=self.eta[sq][st,stt]
      #Get the current probabiltiies
      #getHMMObsLogProb(sq,) seqId,tranP
      #print 'ETA',priorEt,self.eta[sq]
      PrObsCur = self.getHMMObsLogProb(sq,ppPI,self.states)
      for ft in range(K):
        if (vidCount[sq,0]==1) and (self.F[sq,ft]==1):
          continue
        if not (featCount[0,ft]==1 and self.F[sq,ft]==1):
          #First decrement the feat count
          featCount[0,ft]=featCount[0,ft]-self.F[sq,ft]
          vidCount[sq,0] = vidCount[sq,0] -  self.F[sq,ft]
          #Here we sample the F_ik  by using the Eq.15 from Emily nFox et.al., JOINT MODELING OF MULTIPLE TIME SERIES VIA THE BETA PROCESS WITH APPLICATION TO MOTION CAPTURE SEGMENTATION
          #First P(f_ik|F):
          if self.F[sq,ft]==1:
            PrPRatio = (N-featCount[0,ft]+1)/float(featCount[0,ft]+1)
          else:
            PrPRatio = (featCount[0,ft]+1)/float(N-featCount[0,ft]+1)
          #Now get the p(y|...)
          ppE = np.mat(np.copy(ppPI))
          if self.F[sq,ft]==1:
            #print 'Before',sq,ft,ppE
            ppE[:,ft]=0.0
            ppE[ft,:]=0.0
            ppE[ft,ft]=0.0
            #print 'After',sq,ft,ppE
            PrObsNew = self.getHMMObsLogProb(sq,ppE,self.states)
            #print PrObsNew , PrObsCur,np.log(PrPRatio)
          else:
            #print 'B',ppE,ft
            ppE[:,ft]=np.multiply(priorEt[:,ft],self.F[sq,:].T)
            ppE[ft,:]=np.multiply(priorEt[ft,:],self.F[sq,:])
            ppE[ft,ft]=priorEt[ft,ft]
            #print 'A',ppE,ft
            PrObsNew = self.getHMMObsLogProb(sq,ppE,self.states)
            #print np.log(np.random.rand()), PrObsNew , PrObsCur,np.log(PrPRatio)
          if np.log(np.random.rand()) < PrObsNew - PrObsCur + np.log(PrPRatio):
            #print 'Accept'
            PrObsCur=PrObsNew
            self.F[sq,ft] = 1 - self.F[sq,ft]
            ppPI=np.mat(np.copy(ppE))
            self.eta[sq]=ppPI
            #print 'After',self.eta[sq]
          #Fix the F back
          featCount[0,ft]=featCount[0,ft]+self.F[sq,ft]
          vidCount[sq,0] = vidCount[sq,0] +  self.F[sq,ft]
    return 0

  def calcLogProbF(self,F=0,ext=0):
    # P(F|\gamma,\alpha)
    # Compute probability of observed feature assignment matrix as function of the 2-parameter Indian Buffet Process  using the hyperparams  gamma (mass) and c0 (conc)
    # see eq. 21 of Ghahramani, Griffiths, and Sollich  "Bayesian nonparametric latent feature models" ISBA 8th World Meeting on Bayesian Statistics, 2006

    #Choose only the used features
    #pdb.set_trace()
    if ext==0:
      F=self.F

    (i,j)=np.sum(F,0).nonzero()
    FDummy = F[:,np.asarray(j)[0]]

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
      logProdFactors = logProdFactors + sp.special.betaln( M[0,k], N-M[0,k] + self.c0 )

    Harmonic_N = np.sum(self.c0 / ( self.c0 -1 + np.array(range(1,N+1))))

    return  K*np.log( self.gamma ) + K*np.log(self.c0) - logKh - self.gamma*Harmonic_N  +  logProdFactors

  def calcLogProbZgivenF(self):
    #Compute p(Z|F), it is a dirichelet distribution
    #Compute the sufficient statistics through counting
    tranMat = np.ones((self.F.shape[1],self.F.shape[1]))*self.lamb
    tranMat[np.diag_indices(self.F.shape[1])]=self.kappa+self.lamb
    priorProb = np.sum(sp.special.gammaln(tranMat)) - np.sum(sp.special.gammaln(np.sum(tranMat,1)))

    for vid in self.videos:
      for i in range(len(vid)-1):
        tranMat[vid[i]['state'],vid[i+1]['state']] = tranMat[vid[i]['state'],vid[i+1]['state']] + 1
    #Now compute the likelihood
    return np.sum(sp.special.gammaln(tranMat)) - np.sum(sp.special.gammaln(np.sum(tranMat,1))) - priorProb

  def calcLogProbObsgivenFZ(self):
    #Compute P(X|Z,F), it is a beta distribution
    (N,K)=self.F.shape
    countVid = np.zeros((K,self.numVidObjs))
    countLang = np.zeros((K,self.numLangObjs))
    genCNT = np.zeros(K)
    for vid in self.videos:
      for frame in vid:
        genCNT[frame['state']]+=1
        countVid[frame['state'],:]=countVid[frame['state'],:]+frame['obsV']
        countLang[frame['state'],:]=countLang[frame['state'],:]+frame['obsL']
    obsProb = 0
    for j in range(K):
      obsProb += sum([sp.special.betaln(self.alpha0+countVid[j,i],self.beta0+genCNT[j]-countVid[j,i]) for i in range(self.numVidObjs)])
      obsProb += sum([sp.special.betaln(self.alpha0+countLang[j,i],self.beta0+genCNT[j]-countLang[j,i]) for i in range(self.numLangObjs)])
    return obsProb-sp.special.betaln(self.alpha0,self.beta0)

  def sampleNextState(self):
    ts = time.time()
    self.sampleSharedFeats()
    te = time.time()
    print 'Time %2.2f sec' % (te-ts)
    self.sampleUniqueFeatures()# Fix this shit :p
    ts = time.time()
    print 'Time %2.2f sec' % (ts-te)
    self.sampleStateSeq( )
    self.sampleEta()
    self.sampleTheta()
    te = time.time()
    print 'Time %2.2f sec' % (te-ts)

    return 0

  def runBPRecipe(self,problemInstance,videos,F,Theta,TrP):
    self.videos = videos #[[{'state':0,'obsV':V[0][i,:],'obsL':V[1][i,:]} for i in range(V[0].shape[0])] for V in problemInstance['Videos']]
    self.F = np.mat(np.ones((len(videos),1)))

    self.c0 = 1.0
    self.gamma = 2.0
    self.alpha0 = 0.7
    self.beta0 = 0.7
    self.lamb = 1.0
    self.kappa = 5.0

    self.numVidObjs = 2
    self.numLangObjs = 2

    #self.F = np.mat(np.ones((len(problemInstance['Videos']),1))) # All videos are from a single mean
    #self.F = np.mat(np.ones((5,1))) # All videos are from a single mean
    self.nIter = 1000
    self.states = {}
    self.states['v']=[np.ones((1,2))*0.5]
    self.states['l']=[np.ones((1,2))*0.5]
    #Theta
    self.minW = 15
    self.maxW = 45

    print 'GT:',self.F


    self.eta = [np.mat([1]) for i in range(5)]
    #for k in range(5):
    #  (i,j)=(1-F[k,:]).nonzero()
    #  self.eta[k][:,np.asarray(j)[0]]=0
    #  self.eta[k][np.asarray(j)[0],:]=0
    #self.eta = [np.mat(np.ones((self.F.shape[1],self.F.shape[1]))) for k in xrange(len(self.videos))]
    # Compute the probability of F
    for n in range(self.nIter):
      exceptProb = self.calcLogProbF() + self.calcLogProbZgivenF()
      currentProb = exceptProb + self.calcLogProbObsgivenFZ()
      print 'Iteration #%d Log-ProbabilityF,Z: %f Log-Probability Total:%f Number of States:%d' %(n,exceptProb,currentProb,self.F.shape[1])
      print self.F
      self.sampleNextState()
      print self.states
      #print self.F
    return 0
