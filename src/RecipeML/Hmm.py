import numpy as np
import scipy as sp

import pdb

class HMM:
  def __init__(self,dim):
    self.dim=dim
    self.P = np.eye(self.dim)
    self.len = 0
    self.state = [{}]
  def viterbi(self):
    #Return viterbi path
    return 0
  def forwardBackward(self):
    #Run forward backward algorithm to compute ikelihoods
    return 0
  def getP(self):
    return self.P
  def setProblem(self,RepMat,OrdMat,TranProb,InitProb,Len,Obs):
    self.R = RepMat
    self.O = OrdMat
    self.P = TranProb
    self.P0 = InitProb
    self.len = Len
    self.Y = Obs
    self.findStates2Track()
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
    print self.alpha
