import numpy as np
import scipy as sp

import pdb

class HMM:
  def __init__(self,dim):
    self.dim=dim
    self.P = np.eye(self.dim)
    self.len = 0
    self.state = [{}]
    self.fnc={}
  def viterbi(self):
    #Return viterbi path
    return 0
  def forwardBackward(self):
    #Run forward backward algorithm to compute ikelihoods
    return 0
  def getPosterior(self):
    return self.Post
  def setProblem(self,RepMat,OrdMat,TranProb,InitProb,Len,Obs,obsFunc):
    self.R = RepMat
    self.O = OrdMat
    self.P = TranProb
    self.P0 = InitProb
    self.len = Len
    self.Y = Obs
    self.findStates2Track()
    self.fnc['obs']=obsFunc
  def findStates2Track(self):
    Filt = np.sum(self.O,0)>0
    self.s2T= [a for a,b in enumerate(list(Filt)) if b]
  def listAppend(self,i,item,PrevBin,nitem,P0):
    if nitem in self.s2T:
      PrevBin[nitem,0]=1
    for j,k in enumerate(self.alpha[i][nitem]):
        v, = np.asarray((k[1]-PrevBin).T)
        if not np.dot(v,v) > 0:
          #Update probs
          #pdb.set_trace()
          self.alpha[i][nitem][j][0]+=self.P[item,nitem]*P0
          return
    #It does not exist so appen
    self.alpha[i][nitem].append([self.P[item,nitem]*P0,PrevBin])
    return
  def obsProb(self,state,obs):
    return self.fnc['obs'](state,obs)
  def match(self,si,sie,si1,si1e):
    if si1 in self.s2T:
      sie[1][si1,0]=1;
      v, = np.asarray(sie[1].T-si1e[1].T)
      return not np.dot(v,v) > 0
    else:
      v, = np.asarray(sie[1].T-si1e[1].T)
      return not np.dot(v,v) > 0
  def BackwardLoop(self):
    self.beta = [[[] for t in range(self.dim)] for p in self.Y]
    for i in range(len(self.Y)-1,-1,-1):
      if i == len(self.Y)-1:
        for q in range(len(self.alpha[i])):
          for k in self.alpha[i][q]:
            self.beta[i][q].append([1,k[1]])
      else:
        for q in range(len(self.alpha[i])):
          for k in self.alpha[i][q]:
            self.beta[i][q].append([0,k[1]])

    for i in range(len(self.Y)-2,-1,-1):
      for g in range(len(self.alpha[i])):
        for t in range(len(self.alpha[i+1])):
          if (self.R[g,t]==0) and self.P[g,t]>0:
            for gi,gg in enumerate(self.alpha[i][g]):
              for ti,tt in enumerate(self.alpha[i+1][t]):
                if self.match(g,gg,t,tt):
                  self.beta[i][g][gi][0]=self.beta[i][g][gi][0]+self.beta[i+1][t][ti][0]*self.obsProb(t,self.Y[i+1])*self.P[g,t]
    #print self.beta

  def ForwardLoop(self):
    EP = np.mat(np.zeros((self.dim,self.dim)))
    if not self.s2T == []:
      EP[self.s2T,self.s2T]
    for i,y in enumerate(self.Y):
      if i==0:
        #Initial Probabilities
        self.alpha=[[[[self.P0[p,0],EP[:,p]]] for p in range(self.dim)]]
      else:
        #Alpha update equation
        self.alpha.append([[] for p in range(self.dim)])
        for g in range(self.dim):
          for prevSt in self.alpha[i-1][g]:
            #Get all possible future states
            for t in range(self.dim):
              if (self.R[g,t]==0) and (not (self.O*(1-prevSt[1]))[t,0]>0) and self.P[g,t]>0:
                #It is a valid transition
                self.listAppend(i,g,prevSt[1],t,prevSt[0])
      for g in range(self.dim):
        for mi,mk in enumerate(self.alpha[i][g]):
          self.alpha[i][g][mi][0]=self.alpha[i][g][mi][0]*self.obsProb(g,self.Y[i])
    #print self.alpha

  def SmoothForwardBackward(self):
    #self.alpha will hold the final posterior
    self.Post = np.mat(np.zeros((self.dim,len(self.Y))))
    for i,y in enumerate(self.Y):
      for g in range(self.dim):
        pSum = 0
        aSum = 0
        bSum = 0
        for ji,jj in enumerate(self.alpha[i][g]):
          pSum=pSum+self.alpha[i][g][ji][0]*self.beta[i][g][ji][0]
        self.Post[g,i]=pSum
    row_sums = self.Post.sum(axis=0)
    self.Post = self.Post / row_sums
  def runSmoothing(self):
    self.ForwardLoop()
    self.BackwardLoop()
    self.SmoothForwardBackward()
