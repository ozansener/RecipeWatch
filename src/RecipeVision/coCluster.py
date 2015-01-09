from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import SpectralClustering


from ModalDB import *
import numpy as np
import scipy as sp
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
