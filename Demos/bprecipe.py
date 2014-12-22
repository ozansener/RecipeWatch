import glpk
import numpy as np
import matplotlib.pyplot as plt

import Utilities.Evaluation as Evaluation
import RecipeML.Baselines as Baseline
from RecipeML import *
import ArtificialData.generateData



F = np.mat([[1,1,1,0],[0,0,1,1],[0,1,1,1],[0,1,1,0],[1,0,1,1]])
Theta = np.mat([[0.9,0.1,0.1,0.1],[0.1,0.9,0.1,0.1],[0.1,0.1,0.9,0.1],[0.1,0.1,0.1,0.9]])
TrP = np.mat([[1+2.0,2.0,3.0,4.0],[3.0,1+2.0,2.0,1.0],[1.0,1.0,2+2.0,3.0],[1.0,1.0,3.0,1.0+2.0]])

#Proposed Method
NumVisObjs = 2
NumLangObjs = 2

NumVIDS = 5
VidLeng = 20

states = {}
states['v']=[np.zeros((4,2))]
states['l']=[np.zeros((4,2))]
for k in range(4):
  for j in  range(2):
    states['v'][0][k,j]=Theta[2+j,k]
    states['l'][0][k,j]=Theta[j,k]

prevst = 0
st=2
videos=[]
for k in range(5):
  st = k%4
  vidi = []
  for t in range(50):
    stP = TrP[st,:]
    newP=np.multiply(F[k,:],stP)
    stP = newP/float(np.sum(newP,axis=1))
    #print st,stP
    st=np.random.choice(range(4),p=np.array(stP)[0])
    fr = {}
    fr['state']=0
    #fr['gt']=st
    fr['obsV']=[ np.random.binomial(1,states['v'][0][st,0]) ,np.random.binomial(1,states['v'][0][st,1])]
    fr['obsL']=[ np.random.binomial(1,states['l'][0][st,0]) ,np.random.binomial(1,states['l'][0][st,1])]
    vidi.append(fr)
  videos.append(vidi)


print 'GT:',F
print 'GT:',states

#F = np.mat([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]])

#F = np.mat([[1,1,1,0],[0,0,1,1],[0,1,1,1],[0,1,1,0],[1,0,1,1]])

bpR = NPBPSampler()
bpR.runBPRecipe(videos,F,states,TrP)
