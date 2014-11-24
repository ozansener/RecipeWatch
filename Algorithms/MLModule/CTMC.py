import numpy as np
import scipy as sp
import networkx as nx

import sys
import pickle

from Utilities import score,plot

def checkIsMLExist(StateTransitionProbs,HoldingTimes):
  #We will check is there a ML trajectory which is equivalent to \prod_{i=0}^{k-1}P_{s_i,s_{i+1}\lambda_{s_i}>1}
  #We will start with creating an DAG with edge weights log P_{s,s^\prime}\lambda_s
  NumOfStates = StateTransitionProbs.shape[1]
  WeightGraph = np.zeros((NumOfStates,NumOfStates))
  #Check for log(0)
  LogGraph = np.log(StateTransitionProbs)
  LogGraph = np.multiply(LogGraph,np.tile(HoldingTimes,(1,NumOfStates)))
  G=nx.from_numpy_matrix(LogGraph,create_using=nx.DiGraph())
  return not nx.negative_edge_cycle((-1)*G)
  #Check for positive weight cycle
  

def getRandomTrajectory(CNCor,CNOr,HoldingTimes,K):
  NumSTs = CNCor.shape[1]
  totT = 0
  times = []
  states = []
  Obs = np.zeros([NumSTs,1])
  samplState = -1
  while totT<K:
    BS =np.logical_not( (CNCor*Obs+CNOr*Obs) > 0.5*np.ones([NumSTs,1]))
    if not np.any(BS):
      break
    k = np.random.randint(0,NumSTs)
    while (not BS[k,0]) or (k==samplState):
      k = np.random.randint(0,NumSTs)
    samplState = k
    Obs[k,0]=1
    states.append(samplState)
    sampleDur =  int(round(np.random.exponential(HoldingTimes[samplState])))+1
    times.append(sampleDur)
    totT = totT + sampleDur
  SEQ = np.array([0]).reshape(1,1)
  for (j,i) in enumerate(states):
    SEQ=np.concatenate((SEQ,np.tile(np.array([i]).reshape(1,1),(1,times[j]))),axis=1)
  return SEQ[0,1:K+1]
