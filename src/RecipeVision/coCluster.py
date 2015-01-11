from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import SpectralClustering


from ModalDB import *
import numpy as np
import scipy as sp
import scipy.sparse
import scipy.sparse.linalg as salg

import pickle
import glob

class CoCluster:
  def FetchDataFromModalDB(self,ModalClient,featureName='CNNFeatures'):
    """
    Iterate over entire ModalDB, gets all the features. The features should be pre-computed
    """
    A = glob.glob('=*.bn')
    print A
    idxs = []
    feats = []
    for fil in A:
      dat = pickle.load(open(fil,'rb'))
      for vids in dat:
        for feat in vids['Features']:
          idxs.append(vids['name']+'_'+str(feat))
          feats.append(vids['Features'][feat])
      if not ModalClient == 42:
        break
    FeatArray = np.array(feats)
    XX = FeatArray.astype('float64')

    pickle.dump(idxs,open('idxs.bn','wb'))

    self.data_points = XX;
    self.labels_gt = np.loadtxt("mnist2500_labels.txt");
    return 0

  def visualizeClusters(self,outputName):
    """
    Create a 100x100 grid of members of each cluster and save it as an image
    """
    return 0

  def getClusters(self):
    idxs = np.array(range(0,self.PDistMat.shape[0]))
    while len(self.clusters)<100:
      #First let's find the eigenvector corresponding to the largest eigen value
      vals, vecs = sp.sparse.linalg.eigsh(self.PDistMat, k=1,which='LM')
      #Now we will discreteize it to find the best threshold
      sortVals = np.sort(vecs,axis=0)
      tempVals = vecs[:,0].copy()
      binVals = np.ones(tempVals.shape)
      curCost = 0
      bestCost = 0
      for i in range(min(1000,sortVals.shape[0]-1),sortVals.shape[0]):
        curT =sortVals[i,0]
        binVals[tempVals<=curT]=0
        bM = np.mat(binVals).T
        curCost = (bM.T*self.PDistMat*bM)/(bM.T*bM)
        if curCost>bestCost:
          bestCost = curCost
          finVals = binVals.copy()

      indices = np.where(finVals)[0]
      remIndices = np.where(1-finVals)[0]
      self.clusters.append(idxs[indices])
      pickle.dump(self.clusters ,open('pclusters.bnbb','wb'))

      if len(remIndices)<2:
        break

      out1 = self.PDistMat.tocsc()[:,remIndices]
      self.PDistMat = out1.tocsr()[remIndices,:]
      idxs = idxs[remIndices]

  def getPairwiseDistanceMatrix(self):
    """
      It is sloghtly slower but memory efficient, fast implementation is not tractable in terms of memory for such a scale
    """
    self.clusters = []
    dataSize = self.data_points.shape
    self.PDistMat = sp.sparse.csr_matrix((dataSize[0],dataSize[0]))
    for k in range(dataSize[0]):
      CurrentPoint = self.data_points[k,:]
      Dist = sp.spatial.distance.cdist(np.reshape(CurrentPoint,(1,dataSize[1])),self.data_points,'euclidean')
      kMins = []
      kDists = []
      maxD = np.max(Dist)+1
      while len(kMins)<5:
        cMins = np.argmin(Dist)
        kMins.append(cMins)
        kDists.append(Dist[0,cMins])
        Dist[0,cMins]=maxD
      for pt in range(len(kMins)):
        #print kMins[pt],k,self.PDistMat.shape,kDists[pt],pt,kDists
        self.PDistMat[k,kMins[pt]]=kDists[pt]
        self.PDistMat[kMins[pt],k]=kDists[pt]

    #Here we go a bit low-level and apply the e^(-1.x) to the data array
    self.PDistMat.data = np.exp((-1)*self.PDistMat.data)

    pickle.dump(self.PDistMat,open('pdist.bnbb','wb'))

  def runAffinityPropogation(self):
    """
    Run the  affinity propogation algorithm. It is used as a baseline in the paper
    """
    af = AffinityPropagation(preference=-2000000).fit(self.data_points)
    self.labels_ap = af.labels_
    pickle.dump(af.labels_,open('affinity_prop.bn','wb'))
    return 0

  def runSpectralClustering(self):
    """
    Run the basic normalized cut algorithm
    """
    af = SpectralClustering(n_clusters=25,n_neighbors=10, assign_labels='discretize').fit(self.data_points)
    self.labels_ap = af.labels_
    pickle.dump(af.labels_,open('spectral_prop.bn','wb'))
    return 0

  def runCoClustering(self):
    """
    Run the proposed co-clustering algorithm
    """
    return 0
  def runDBSCAN(self):
    """
      Run the DBSCAN Clustering algorithm
    """
    X = StandardScaler().fit_transform(self.data_points)

    ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    self.labels_db = db.labels_

  def evaluateAllAlgorithms(self):
    algs = [self.labels_db,self.labels_ap]
    tits =['DBASE','AP']
    for i in range(2):
      print 'Algorithm:',tits[i]
      print("\tHomogeneity: %0.3f" % metrics.homogeneity_score(self.labels_gt, algs[i]))
      print("\tCompleteness: %0.3f" % metrics.completeness_score(self.labels_gt, algs[i]))
      print("\tV-measure: %0.3f" % metrics.v_measure_score(self.labels_gt, algs[i]))
      print("\tAdjusted Rand Index: %0.3f"% metrics.adjusted_rand_score(self.labels_gt, algs[i]))
      print("\tAdjusted Mutual Information: %0.3f"% metrics.adjusted_mutual_info_score(self.labels_gt, algs[i]))
