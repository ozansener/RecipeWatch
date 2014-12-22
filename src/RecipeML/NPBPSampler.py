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
    #pdb.set_trace()
    #self.eta = [np.mat(np.zeros((self.F.shape[1],self.F.shape[1]))) for k in xrange(len(self.videos))]
    #We will sample eta for each videos
    for numV,vid in enumerate(self.videos):
    #Start with collecting the sufficient statistics
      tranMat = np.mat(np.ones((self.F.shape[1],self.F.shape[1]))*self.lamb)
      tranMat[np.diag_indices(self.F.shape[1])]=self.kappa+self.lamb
      for i in range(len(vid)-1):
        tranMat[vid[i]['state'],vid[i+1]['state']] = tranMat[vid[i]['state'],vid[i+1]['state']] + 1

      #Get only the selected features
      i,j=self.F[numV,:].nonzero()
      selFeats = np.array(j).reshape(-1,).tolist()
      self.eta[numV]=np.mat(np.zeros((self.F.shape[1],self.F.shape[1])))
      for x in selFeats:
        for y in selFeats:
          self.eta[numV][x,y]=np.random.gamma(tranMat[x,y])
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
    #pdb.set_trace()
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
    #pdb.set_trace()
    (i,j)=self.F[sq,:].nonzero()
    j=np.asarray(j)[0]
    #preComputedEtaa=np.mat(np.zeros((len(j),len(j))))
    preComputedEtaa=self.eta[sq][j,:][:,j]

    seq2 = HMMFast(len(j))

    POST= seq2.sampleFast(preComputedEtaa,self.obsPreComputedLikelihoods[sq][j,:])

    for t in range(len(self.videos[sq])):
      POST[t]=j[POST[t]]
      self.videos[sq][t]['state']=POST[t]
    return POST

  def getFastHMMLikelihood(self,states,unNormalizedTranP,sqId,ObsLikelihoods):
    #pdb.set_trace()
    seq2 = HMMFast(ObsLikelihoods.shape[0])
    return seq2.runCachedSmoothing(unNormalizedTranP,ObsLikelihoods)



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
  def sampleUniqueFeatures(self):
    #pdb.set_trace()
    #For each video
    (N,K) = self.F.shape
    #Most of the statistics are already coll
    for sq in range(N):
      (N,K) = self.F.shape
      preComputedEta = {}
      featCount = np.sum(self.F,axis=0)
      vidCount = np.sum(self.F,axis=1)
      uniqueL=[]
      for kk in range(K):
        if featCount[0,kk]==1 and self.F[sq,kk]==1:
          uniqueL.append(kk)
      #First compute the old probability anyway
      (i,j)=self.F[sq,:].nonzero()
      j=np.asarray(j)[0]
      TranNew = self.eta[sq][j,:][:,j]
      StateNew= {}
      StateNew['v'] = self.states['v'][0][j,:]
      StateNew['l'] = self.states['l'][0][j,:]

      preComputedEta[sq]=np.mat(np.random.gamma(np.ones((K,K))*self.lamb+np.eye(K)*self.kappa))
      for x in j:
        for y in j:
          preComputedEta[sq][x,y]=self.eta[sq][x,y]

      oldProb = self.getFastHMMLikelihood(StateNew,TranNew,sq,self.obsPreComputedLikelihoods[sq][j,:])

      if (len(uniqueL)==0 or np.random.rand()>0.5) :
        #Birth
        #First choose data driven window length
        vid = self.videos[sq]
        if self.minW < len(vid):
          leng = int(np.random.uniform(self.minW,min(self.maxW,len(vid)-1)))
        else:
          leng = int(np.random.uniform(1,min(self.maxW,len(vid)-1)))
        startP = int(np.random.uniform(0,len(vid)-leng-1))


        F = np.concatenate((self.F,np.zeros((self.F.shape[0],1))),axis=1)
        F[sq,self.F.shape[1]]=1

        preComputedEta[sq]=np.mat(np.random.gamma(np.ones((K+1,K+1))*self.lamb+np.eye(K+1)*self.kappa))
        (i,j)=F[sq,:].nonzero()
        j = np.asarray(j)[0]
        for x in j[:-1]:
          for y in j[:-1]:
            preComputedEta[sq][x,y]=self.eta[sq][x,y]

        TranNew = preComputedEta[sq][j,:][:,j]
        #PopulateNew Row
        self.obsPreComputedLikelihoods[sq] = np.concatenate((self.obsPreComputedLikelihoods[sq],np.zeros((1,len(self.videos[sq])))),axis=0 )

        #print self.states
        ThetaNew = self.mlTheta(sq,startP,startP+leng+1,F,self.F.shape[1])
        for x in range(self.F.shape[1]):
          ThetaNew['v'][0][x,:]=self.states['v'][0][x,:]
          ThetaNew['l'][0][x,:]=self.states['l'][0][x,:]
        #print ThetaNew,self.obsPreComputedLikelihoods[sq].shape

        for t in range(len(self.videos[sq])):
          kk=K
          self.obsPreComputedLikelihoods[sq][kk,t]=np.sum(np.log([ThetaNew['v'][0][kk,i]*self.videos[sq][t]['obsV'][i]+(1-ThetaNew['v'][0][kk,i])*(1-self.videos[sq][t]['obsV'][i]) for i in range(self.numVidObjs)]))
          self.obsPreComputedLikelihoods[sq][kk,t]+=np.sum(np.log([ThetaNew['l'][0][kk,i]*self.videos[sq][t]['obsL'][i]+(1-ThetaNew['l'][0][kk,i])*(1-self.videos[sq][t]['obsL'][i]) for i in range(self.numLangObjs)]))

        newProb = self.getFastHMMLikelihood(ThetaNew,TranNew,sq,self.obsPreComputedLikelihoods[sq][j,:])

        etaa = self.gamma *1.0/(1.0 + N -1.0 );
        logPrNumFeat_Diff = np.log( etaa ) +  sp.special.gammaln( F.shape[1] -1) - sp.special.gammaln( F.shape[1]  );

        #pdb.set_trace()
        if np.exp(newProb - oldProb + logPrNumFeat_Diff - np.log(0.5) + np.log(0.5/(len(uniqueL)+1.0))) > np.random.rand():
          self.F = F

          self.states['v'][0]=np.concatenate((self.states['v'][0],ThetaNew['v'][0][-1,:]),axis=0)
          self.states['l'][0]=np.concatenate((self.states['l'][0],ThetaNew['v'][0][-1,:]),axis=0)

          self.eta[sq]=np.concatenate((self.eta[sq],preComputedEta[sq][:-1,-1]),axis=1)
          self.eta[sq]=np.concatenate((self.eta[sq],preComputedEta[sq][-1,:]),axis=0)

          #Update the next ones
          L1 =range(len(self.videos))
          L1.remove(sq)
          for vi in L1:
            self.eta[vi]=np.concatenate((self.eta[vi],np.zeros((self.eta[vi].shape[0],1))),axis=1)
            self.eta[vi]=np.concatenate((self.eta[vi],np.zeros((1,self.eta[vi].shape[1]))),axis=0)
            self.obsPreComputedLikelihoods[vi] = np.concatenate((self.obsPreComputedLikelihoods[vi],np.zeros((1,len(self.videos[vi])))),axis=0 )

            for t in range(len(self.videos[vi])):
              kk=K
              self.obsPreComputedLikelihoods[vi][kk,t]=np.sum(np.log([self.states['v'][0][kk,i]*self.videos[vi][t]['obsV'][i]+(1-self.states['v'][0][kk,i])*(1-self.videos[vi][t]['obsV'][i]) for i in range(self.numVidObjs)]))
              self.obsPreComputedLikelihoods[vi][kk,t]+=np.sum(np.log([self.states['l'][0][kk,i]*self.videos[vi][t]['obsL'][i]+(1-self.states['l'][0][kk,i])*(1-self.videos[vi][t]['obsL'][i]) for i in range(self.numLangObjs)]))
        else:
          self.obsPreComputedLikelihoods[sq]=np.delete(self.obsPreComputedLikelihoods[sq],K,0)
          #print 'SPB',self.F.shape[1],self.states
          #update eta,theta
      elif (vidCount[sq,0]>1):
        #Death
        feat2kill = np.random.choice(uniqueL)

        self.F[sq,feat2kill]=0

        (i,j)=self.F[sq,:].nonzero()
        j = np.asarray(j)[0]

        preComputedEta[sq]=np.mat(np.random.gamma(np.ones((K,K))*self.lamb+np.eye(K)*self.kappa))
        preComputedEta[sq][j,:][:,j]=self.eta[sq][j,:][:,j]
        TranNew = preComputedEta[sq][j,:][:,j]

        StateNew = {}
        StateNew['v']=[self.states['v'][0][j,:]]
        StateNew['l']=[self.states['l'][0][j,:]]

        newProb = self.getFastHMMLikelihood(StateNew,TranNew,sq,self.obsPreComputedLikelihoods[sq][j,:])

        etaa = self.gamma *1.0/(1.0 + N -1.0 );
        logPrNumFeat_Diff = -np.log( etaa ) -  sp.special.gammaln( self.F.shape[1]-1 ) + sp.special.gammaln( self.F.shape[1] );
        if np.exp(newProb - oldProb + logPrNumFeat_Diff-np.log(0.5/len(uniqueL))+np.log(0.5))> np.random.rand():
          #accept
          newF= self.F[:,range(0,feat2kill)+range(feat2kill+1,self.F.shape[1])]
          self.F = newF

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
            self.obsPreComputedLikelihoods[vi]=np.delete(self.obsPreComputedLikelihoods[vi],feat2kill,0)
        else:
          self.F[sq,feat2kill]=1
    return 0
  def sampleSharedFeats(self):
    #pdb.set_trace()
    #We only sample the columns who has more than one video to support it. In other words, we do not sample features unqiue to a specific video.
    #First compute the number of occurences of each feature
    featCount = np.sum(self.F,axis=0)
    vidCount = np.sum(self.F,axis=1)
    (N,K) = self.F.shape

    #For computational efficiency we first cache all likelihoods and eta's
    self.obsPreComputedLikelihoods = {}
    preComputedEta = {}
    for sq in range(N):
      #Cache likelihoods
      self.obsPreComputedLikelihoods[sq]=np.zeros((K,len(self.videos[sq])))
      for t in range(len(self.videos[sq])):
        for kk in range(K):
          self.obsPreComputedLikelihoods[sq][kk,t]=np.sum(np.log([self.states['v'][0][kk,i]*self.videos[sq][t]['obsV'][i]+(1-self.states['v'][0][kk,i])*(1-self.videos[sq][t]['obsV'][i]) for i in range(self.numVidObjs)]))
          self.obsPreComputedLikelihoods[sq][kk,t]+=np.sum(np.log([self.states['l'][0][kk,i]*self.videos[sq][t]['obsL'][i]+(1-self.states['l'][0][kk,i])*(1-self.videos[sq][t]['obsL'][i]) for i in range(self.numLangObjs)]))
      #Cache ETAs
      preComputedEta[sq]=np.mat(np.random.gamma(np.ones((K,K))*self.lamb+np.eye(K)*self.kappa))
      (i,j)=self.F[sq,:].nonzero()
      j = np.asarray(j)[0]
      for x in j:
        for y in j:
          preComputedEta[sq][x,y]=self.eta[sq][x,y]
    #pdb.set_trace()
    for sq in range(N):
      PrObsCur = 1
      for ft in range(K):
        if (vidCount[sq,0]==1) and (self.F[sq,ft]==1):
          continue
        if (featCount[0,ft]==1 and self.F[sq,ft]==1):
          continue

        if PrObsCur == 1:
          (i,j)=self.F[sq,:].nonzero()
          j = np.asarray(j)[0]
          TranNew = preComputedEta[sq][j,:][:,j]
          StateNew= {}
          StateNew['v'] = self.states['v'][0][j,:]
          StateNew['l'] = self.states['l'][0][j,:]
          PrObsCur = self.getFastHMMLikelihood(StateNew,TranNew,sq,self.obsPreComputedLikelihoods[sq][j,:])

        #First decrement the feat count
        featCount[0,ft]=featCount[0,ft]-self.F[sq,ft]
        vidCount[sq,0] = vidCount[sq,0] -  self.F[sq,ft]

        if self.F[sq,ft]==1:
          PrPRatio = (N-featCount[0,ft])/float(featCount[0,ft])
        else:
          PrPRatio = (featCount[0,ft])/float(N-featCount[0,ft])
        #Here we sample the F_ik  by using the Eq.15 from Emily nFox et.al., JOINT MODELING OF MULTIPLE TIME SERIES VIA THE BETA PROCESS WITH APPLICATION TO MOTION CAPTURE SEGMENTATION


        self.F[sq,ft]=1-self.F[sq,ft]
        (i,j)=self.F[sq,:].nonzero()
        j = np.asarray(j)[0]
        TranNew = preComputedEta[sq][j,:][:,j]
        StateNew= {}
        StateNew['v'] = self.states['v'][0][j,:]
        StateNew['l'] = self.states['l'][0][j,:]
        PrObsNew = self.getFastHMMLikelihood(StateNew,TranNew,sq,self.obsPreComputedLikelihoods[sq][j,:])

        if  np.exp(PrObsNew - PrObsCur)*PrPRatio > np.random.rand():
          PrObsCur = PrObsNew
          if self.F[sq,ft]==1:
            for x in j:
              self.eta[sq][x,ft]=preComputedEta[sq][x,ft]
              self.eta[sq][ft,x]=preComputedEta[sq][ft,x]
          else:
            for x in j:
              self.eta[sq][x,ft]=0
              self.eta[sq][ft,x]=0
            self.eta[sq][ft,ft]=0
        else:
          self.F[sq,ft]=1-self.F[sq,ft]

        featCount[0,ft] = featCount[0,ft]+self.F[sq,ft]
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
    return obsProb-K*sp.special.betaln(self.alpha0,self.beta0)

  def sampleNextState(self):
    #pdb.set_trace()
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

  def runBPRecipe(self,videos,F,Theta,TrP):
    self.videos = videos #[[{'state':0,'obsV':V[0][i,:],'obsL':V[1][i,:]} for i in range(V[0].shape[0])] for V in problemInstance['Videos']]
    self.F = np.mat(np.ones((len(videos),1)))

    self.c0 = 1.0
    self.gamma = 1.01
    self.alpha0 = 0.7
    self.beta0 = 0.7
    self.lamb = 1.0
    self.kappa = 2.0

    self.numVidObjs = 2
    self.numLangObjs = 2

    #self.F = np.mat(np.ones((len(problemInstance['Videos']),1))) # All videos are from a single mean
    #self.F = np.mat(np.ones((5,1))) # All videos are from a single mean
    self.nIter = 300
    self.states = {}
    self.states['v']=[np.ones((1,2))*0.5]
    self.states['l']=[np.ones((1,2))*0.5]
    #Theta
    self.minW = 2
    self.maxW = 9

    print 'GT:',self.F


    self.eta = [np.mat([2.0]) for i in range(len(videos))]
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
