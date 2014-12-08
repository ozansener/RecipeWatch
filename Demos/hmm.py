from RecipeML import *
import numpy as np

#Observation function is not just a matrix, it can be more complicated so it is a function pointer
def oF(st,obs):
  EP = np.mat([[0.5,0.4,0.1],[0.1,0.3,0.6],[0,0,0]])
  return EP[st,obs]


seq1 = HMM(3) #Hmm with 3 states
#Transition probabilities
TRP =np.mat([[0.69,0.3,0.01],[0.4,0.59,0.01],[0,0,1]])
#Initial state
pi0 = np.mat([[0.6,0.4,0]]).T

#Set the problem
seq1.setProblem(np.zeros((3,3)),np.zeros((3,3)),TRP,pi0,3,[0,1,2],oF)
#Run Forward-Backward Algorithm
seq1.runSmoothing()
#Print the posterior
print seq1.getPosterior()
