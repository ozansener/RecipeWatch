import glpk
import numpy as np
import matplotlib.pyplot as plt
import pdb
import scipy
import scipy.optimize

numVidObjs = 10
numVideos = 100
numStates = 5

coNot = np.mat([[0,0,1,0,0],[0,0,0,0,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
coNot = coNot.T+coNot
print coNot

tranP = np.mat(np.random.dirichlet([1,1,1,1,1],5))

obsProb = np.random.beta(0.5,0.5,[5,10])

VS = {}
for i in range(numVideos):
  prevBn = np.mat(np.zeros((5,1)))
  prevSt = i % 5
  prevBn[prevSt]=1
  VS[0,0]=0
  for t in range(100):
    PS = np.multiply((1-coNot*prevBn).T,tranP[prevSt,:])
    stT,=np.asarray(PS / np.sum(PS,1))
    st = np.nonzero(np.random.multinomial(1,stT,1))[1][0]
    VS[i,t]=st
    prevSt = st
    prevBn[prevSt]=1
print 'N'

VO = {}
for i in range(100):
  for t in range(100):
    VO[i,t]=[0]*10
    for l in range(10):
      if np.random.rand()>obsProb[VS[i,t],l]:
        VO[i,t][l]=1

COP = np.zeros((10,10))
NOP = np.zeros((10,1))

print 'NN'

for i in range(100):
  print i
  for t in range(100):
    for l in range(10):
      if VO[i,t][l]==1:
        NOP[l,0]+=1
      for n in range(t+1,100):
        for ll in range(10):
          if VO[i,t][l] == VO[i,n][ll] and  1 == VO[i,n][ll]:
            COP[l,ll]+=1
            COP[ll,l]+=1

#for l in range(10):
#  for ll in range(10):
#s    COP[l,ll]=COP[l,ll]/(NOP[l,0]*NOP[ll,0])


#Here the algorithm starts
BVEC = COP.reshape(np.prod(COP.shape))
STT = np.mat(obsProb).T
sh=STT.shape
AMAT = np.multiply(np.kron(np.ones(sh),STT),np.kron(STT,np.ones(sh)))


CNN = scipy.optimize.nnls(AMAT, BVEC)[0].reshape(5,5)
for k in range(5):
  for kk in range(5):
    if not k == kk:
      if CNN[k,k]==0 or CNN[kk,kk]==0:
        CNN[k,kk] = 1
      else:
          CNN[k,kk]=CNN[k,kk]/np.sqrt(CNN[k,k]*CNN[kk,kk])

for k in range(5):
  CNN[k,k]=1
print 1-((CNN+CNN.T)/2)
#And here it ends
