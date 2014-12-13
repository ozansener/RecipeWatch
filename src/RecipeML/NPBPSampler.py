import numpy as np
import scipy as sp

class NPBPSampler:
  def sampleTheta(self):
    #1st sample visual occurances
    #Collect the sufficient statistics
    numStates =
    numVidObjs =
    numHistBins =
    countStates = np.zeros(numStates)
    countStatistics = np.zeros((numStates,numVidObjs))
    histStatistics = np.mat(np.zeros((numStates,numVidObjs,numHistBins)))
    for vid in Videos:
      for frame in vid:
        countStates[frame['z']]+=1
        countStatistics[frame['z'],:]+=frame['objOcc']
        lanStatistics[frame['z'],:]+=frame['wordCounts']
        for j in range(numVidObjs):
          if frame['y'][j][0]:
            histStatistics[frame['z'],j,frame['y'][j][1]]+=1
    #Sample the beta varaible
    for k in range(numStates):
      for j in  range(numVidObjs):
        states['v'][k][j][0]=np.random.beta(alpha0+countStatistics[k,j],beta0+(countStates[k]-countStatistics[k,j]),1)[0]
        states['v'][k][j][1]=np.random.dirichlet(alphaFlow+histStatistics[k,j,:])

    #2nd sample language occurances
    for k in range(numStates):
      for j in range(numLanObjs):
        states['l'][k][j]=np.random.drichlet(alphaLan+lanStatistics[k,:])
  def solveFactorization(self):
    return 0
  def sampleCoMatrices(self):
    return 0
  def sampleStates(self):
    return 0
  def sampleBPHyperParams(self):
    return 0
  def sampleHMMHyperParams(self):
    return 0
  def sampleUniqueFeatures(self):
    return 0
  def sampleSharedFeatures(self):
    return 0
