from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from ModalDB import *
import numpy as np
import scipy as sp

class CoCluster:
  def FetchDataFromModalDB(self,ModalClient,featureName='CNNFeatures'):
    """
    Iterate over entire ModalDB, gets all the features. The features should be pre-computed
    """
    self.data_points = np.loadtxt("mnist2500_X.txt");
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
    af = AffinityPropagation(preference=-600).fit(self.data_points)
    self.labels_ap = af.labels_
    return 0

  def runSpectralClustering(self):
    """
    Run the basic normalized cut algorithm
    """
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
