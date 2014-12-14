import glpk
import numpy as np
import matplotlib.pyplot as plt

import Utilities.Evaluation as Evaluation
import RecipeML.Baselines as Baseline
from RecipeML import *
import ArtificialData.generateData


NumVisObjs = 10
NumLangObjs = 15
NumVIDS = 100
NumSTs = 20
noise=0.3
plotting = False
fileName=''


Problem = ArtificialData.generateData.getArtificialProblem(NumVisObjs,NumLangObjs,NumVIDS,NumSTs,noise,plotting,fileName)


GT = Problem['Videos'][0][2]
for i in xrange(1,len(Problem['Videos'])):
  GT=np.concatenate((GT,Problem['Videos'][i][2]),axis=0)

#Proposed Method
bpR = NPBPSampler()
bpR.runBPRecipe(Problem)

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
