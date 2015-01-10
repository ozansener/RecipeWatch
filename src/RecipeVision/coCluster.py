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

  def getPairwiseDistanceMatrix(self):
    """
      It is sloghtly slower but memory efficient, fast implementation is not tractable in terms of memory for such a scale
    """
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
