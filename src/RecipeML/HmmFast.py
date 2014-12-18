import numpy as np
import scipy as sp

import pdb

class HMMFast:
  def __init__(self,dim):
    self.dim=dim
    self.P = np.eye(self.dim)
    self.len = 0
    self.state = [{}]
    self.fnc={}
  def ForwardPass(self):
    L = self.len
    self.alpha = np.zeros((self.len,self.dim))
    # forward part of the algorithm
    for i in range(self.len):
        f_curr = {}
        for st in range(self.dim):
            if i == 0:
                # base case for the forward part
                prev_f_sum = self.P0[st]
            else:
                prev_f_sum = sum(self.alpha[i-1,k]*self.P[k,st] for k in range(self.dim))

            self.alpha[i,st]=prev_f_sum*self.obsProb(st,self.Y[i])

  def BackwardPass(self):
    L = self.len
    self.beta = np.zeros((self.len,self.dim))
    for i in range(self.len):
      # backward part of the algorithm
      for i in range(self.len-1,-1,-1):
          for st in range(self.dim):
              if i == (self.len-1):
                  # base case for backward part
                  self.beta[i,st] = 1
              else:
                  self.beta[i,st] = sum(self.P[st,l]* self.obsProb(l,self.Y[i+1])*self.beta[i+1,l] for l in range(self.dim))

  def getPosterior(self):
    return self.Post
  def setProblem(self,RepMat,OrdMat,TranProb,InitProb,Len,Obs,obsFunc):
    self.R = RepMat
    self.O = OrdMat
    self.P = TranProb
    self.P0 = InitProb
    self.len = Len
    self.Y = Obs
    self.fnc['obs']=obsFunc
  def obsProb(self,state,obs):
    return self.fnc['obs'](state,obs)

  def getSample(self):
    self.BackwardPass()
    samp = []
    PR = np.zeros(self.dim)
    for j in range(self.dim):
      PR[j]= self.P0[j]
    PR = np.multiply(PR,self.beta[0,:])
    PR = PR/np.sum(PR)
    samp.append(np.random.choice(range(self.dim),p=PR))
    for t in range(1,self.len):
      PR = self.beta[t,:]
      PR = np.multiply(PR,np.asarray(self.P[samp[t-1],:])[0])
      #print PR,self.dim
      for j in range(self.dim):
        PR[j]=PR[j]*self.obsProb(j,self.Y[t])
      PR = PR/np.sum(PR)
      samp.append(np.random.choice(range(self.dim),p=PR))
    return samp
  def SmoothForwardBackward(self):
    #self.alpha will hold the final posterior
    self.Post = np.mat(np.zeros((self.dim,len(self.Y))))
    for i,y in enumerate(self.Y):
      for g in range(self.dim):
        pSum = 0
        aSum = 0
        bSum = 0
        self.Post[g,i]=self.alpha[i,g]*self.beta[i,g]
    row_sums = self.Post.sum(axis=0)
    self.Post = self.Post / row_sums
  def runSmoothing(self):
    self.ForwardPass()
    self.BackwardPass()
    self.SmoothForwardBackward()
