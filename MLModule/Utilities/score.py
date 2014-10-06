import numpy as np
import scipy as sp

import pdb

def getMinIou(gt,ar_id,vidLen):
  cur = 0
  tot = 0
  #pdb.set_trace()
  Z = vidLen.shape[0]
  for k in range(Z):
    gtt = gt[cur:cur+vidLen[k],0]
    ar_idd = ar_id[cur:cur+vidLen[k]]
    t_iou =0
    for i in set(gtt):
      m_iou = 0
      id_i = np.nonzero(gtt==i)
      for j in set(ar_idd):
        id_j = np.nonzero(ar_idd==j)
        l_iou = float(len(np.intersect1d(id_i[0],id_j[0])))/float(len(np.union1d(id_i[0],id_j[0])))
        if l_iou > m_iou:
          m_iou = l_iou
      t_iou = t_iou + m_iou
    if len(set(gtt)) > 0:
      tot = tot + t_iou/len(set(gtt))
    else:
      Z=Z-1
    cur = cur + vidLen[k]
  #  pdb.set_trace()

  return tot/vidLen.shape[0]
