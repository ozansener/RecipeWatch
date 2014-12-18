import glpk
import numpy as np
import matplotlib.pyplot as plt

import Utilities.Evaluation as Evaluation
import RecipeML.Baselines as Baseline
from RecipeML import *
import ArtificialData.generateData


NumVisObjs = 2
NumLangObjs = 2
NumVIDS = 5
NumSTs = 20
noise=0.3
plotting = False
fileName=''


Problem = ArtificialData.generateData.getArtificialProblem(NumVisObjs,NumLangObjs,NumVIDS,NumSTs,noise,plotting,fileName)



GT = Problem['Videos'][0][2]
for i in xrange(1,len(Problem['Videos'])):
  GT=np.concatenate((GT,Problem['Videos'][i][2]),axis=0)



F = np.mat([[1,1,1,0],[0,0,1,1],[0,1,1,1],[0,1,1,0],[1,0,1,1]])



Theta = np.mat([[0.9,0.9],[0.9,0.2],[0.2,0.9],[0.2,0.2]])
TrP = np.mat([[1+5.0,2.0,3.0,4.0],[3.0,1+5.0,2.0,1.0],[1.0,1.0,2+5.0,3.0],[1.0,1.0,3.0,1.0+5.0]])
#Proposed Method
NumVisObjs = 2
NumLangObjs = 2

NumVIDS = 5
VidLeng = 10

states = {}
states['v']=[np.zeros((4,2))]
states['l']=[np.zeros((4,2))]
for k in range(4):
  for j in  range(2):
    states['v'][0][k,j]=np.random.beta(0.7,0.7,1)[0]
    states['l'][0][k,j]=np.random.beta(0.7,0.7,1)[0]


#ThetaT = np.mat([[1,1],[1,0],[0,1],[0,0]])

prevst = 0
st=2
videos=[]
for k in range(5):
  st = k%4
  vidi = []
  for t in range(10):
    stP = TrP[st,:]
    newP=np.multiply(F[k,:],stP)
    stP = newP/float(np.sum(newP,axis=1))
    #print st,stP
    st=np.random.choice(range(4),p=np.array(stP)[0])
    fr = {}
    fr['state']=0
    #fr['gt']=st
    fr['obsV']=[ np.random.binomial(1,states['v'][0][st,0]) ,np.random.binomial(1,states['v'][0][st,0])]
    fr['obsL']=[ np.random.binomial(1,states['v'][0][st,0]) ,np.random.binomial(1,states['v'][0][st,0])]
    vidi.append(fr)
  videos.append(vidi)


print 'GT:',F
print 'GT:',states

F = np.mat([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]])

#F = np.mat([[1,1,1,0],[0,0,1,1],[0,1,1,1],[0,1,1,0],[1,0,1,1]])

bpR = NPBPSampler()
bpR.runBPRecipe(Problem,videos,F,states,TrP)

exit(0)
#K-Means with good K
Dat,idS = Baseline.ApplyKMeansToProblem(Problem,20)
scGoodK = Evaluation.getMinIou(GT,idS,Problem['VideoLength'])

scBadK=0
for dummy in xrange(50):
  Dat,idS = Baseline.ApplyKMeansToProblem(Problem,np.random.geometric(0.05))
  scBadK = scBadK+ Evaluation.getMinIou(GT,idS,Problem['VideoLength'])
print scGoodK,scBadK/50

#Compute F
#Compute
#            #
#            #
#            #
# BASELINES  #
#            #
#            #
#            #
#K-Means + HMM
#Oracle: Correct TranP,StateMeans,Wrong, CoNot
#Oracle^2: Correct TranP,StateMeans, CoNot

# return {'Durations':Dur,'CoNotOccur':CNCor,'CoNotOrder':CNOr,'VisualMeans':sv,'LanguageMeans':sl,'Videos':VidL,'VideoLength':vidLengths}
