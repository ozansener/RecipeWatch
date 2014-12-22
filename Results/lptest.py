import glpk
import numpy as np
import matplotlib.pyplot as plt

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
  prevSt = 0
  VS[0,0]=0
  for t in range(100):
    stT,=np.asarray(np.multiply((1-coNot[prevSt,:]),tranP[prevSt,:]))
    st = np.nonzero(np.random.multinomial(1,stT,1))[1][0]
    VS[i,t]=st
    prevSt = st

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

print 'NNN'

#for l in range(10):
#  for ll in range(10):
#    COP[l,ll]=COP[l,ll]/(NOP[l,0]*NOP[ll,0])

A= obsProb.T*(1-coNot)*obsProb

column_labels = list('0123456789')
row_labels = list('0123456789')

A = np.asarray(A)
#row_sums = A.sum(axis=0)
#A = A / row_sums

fig, ax = plt.subplots()
heatmap = ax.pcolor(A, cmap=plt.cm.Blues)


print heatmap
# put the major ticks at the middle of each cell
print np.arange(A.shape[1])+0.5
print A.shape
ax.set_xticks(np.arange(A.shape[0])+0.5, minor=False)
ax.set_yticks(np.arange(A.shape[1])+0.5, minor=False)

ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels, minor=False)
plt.savefig('abc.png')



A= COP

column_labels = list('0123456789')
row_labels = list('0123456789')

A = np.asarray(A)
#row_sums = A.sum(axis=0)
#A = A / row_sums

fig, ax = plt.subplots()
heatmap = ax.pcolor(A, cmap=plt.cm.Blues)


print heatmap
# put the major ticks at the middle of each cell
print np.arange(A.shape[1])+0.5
print A.shape
ax.set_xticks(np.arange(A.shape[0])+0.5, minor=False)
ax.set_yticks(np.arange(A.shape[1])+0.5, minor=False)

ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(column_labels, minor=False)
plt.savefig('abc2.png')
