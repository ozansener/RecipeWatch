import numpy as np
import scipy as sp

class Evaluation:
  def getMinIou(gt,ar_id,vidLen):
    # Compute IOU score
    # Since the algorithm is unsupervised find the minimum score
    cur = 0
    tot = 0
    Z = vidLen.shape[0] #For each video
    for k in range(Z):
      gtt = gt[cur:cur+vidLen[k],0] #Ground truth result
      ar_idd = ar_id[cur:cur+vidLen[k]] #Prediciton result
      t_iou =0
      for i in set(gtt): #For each segment available in the current video
        m_iou = 0
        id_i = np.nonzero(gtt==i)
        for j in set(ar_idd):
          id_j = np.nonzero(ar_idd==j)
          l_iou = float(len(np.intersect1d(id_i[0],id_j[0])))/float(len(np.union1d(id_i[0],id_j[0])))
          if l_iou > m_iou:
            m_iou = l_iou #find the optimistic IO
        t_iou = t_iou + m_iou
      if len(set(gtt)) > 0:
        tot = tot + t_iou/len(set(gtt))
      else:
        Z=Z-1
      cur = cur + vidLen[k]
    #  pdb.set_trace()

    return tot/vidLen.shape[0] #return mean of the IOU
