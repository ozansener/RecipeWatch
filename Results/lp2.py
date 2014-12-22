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

BVEC = COP.reshape(np.prod(COP.shape))
STT = np.mat(obsProb).T
sh=STT.shape
AMAT = np.multiply(np.kron(np.ones(sh),STT),np.kron(STT,np.ones(sh)))

lamb = 0.0000000000000000001

lp = glpk.LPX()        # Create empty problem instance
lp.name = 'conot'     # Assign symbolic name to problem
lp.obj.maximize = False # Set this as a maximization problem
NumR = np.prod(BVEC.shape)
lp.rows.add(2*NumR)         # Append three rows to this instance
for i in range(NumR):
  lp.rows[i].bounds = None,BVEC[i]
  lp.rows[i+NumR].bounds = None,(-1)*BVEC[i]


lp.cols.add(AMAT.shape[1]+NumR)         # Append three columns to this instance
for c in lp.cols:      # Iterate over all columns
	c.bounds = 0.0, None     # Set bound 0 <= xi < inf


lp.obj[:] =  list(np.ones(NumR))+ list(lamb*np.ones(AMAT.shape[1]))# Set objective coefficients

M1=np.concatenate([(-1)*np.eye(NumR),AMAT],axis=1)
M2=np.concatenate([(-1)*np.eye(NumR),(-1)*AMAT],axis=1)
M = np.concatenate([M1,M2],axis=0)

MA, = np.asarray(M.reshape(np.prod(M.shape)))

lp.matrix = list(MA)
lp.simplex()           # Solve this LP with the simplex method
print 'Z = %g;' % lp.obj.value,  # Retrieve and print obj func value
ls = [c.primal for c in lp.cols]
CN = np.mat(ls[NumR:]).reshape(5,5)
print obsProb
print coNot
print CN

print ls[1:NumR]


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
