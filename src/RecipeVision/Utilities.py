import numpy as np
from ModalDB import Frame
import matplotlib.pyplot as plt

import scipy as sp
import scipy.ndimage

import caffeCNN

def segmentTheFrame(InputFrame):
  """
    Given a frame, computes maximum 10 non-overlapping masks. Non-overlapping means having a less than 50percent overlap
    It returns the selected mask ids and masks
  """
  maxMask = 100
  idXs = []
  masks = []
  numM = InputFrame['masks'].shape[2]
  currentlyCovered = np.zeros((InputFrame['masks'].shape[0],InputFrame['masks'].shape[1]))>1
  for k in range(min(numM,maxMask)):
    M = InputFrame['masks'][:,:,k]>0
    if np.sum(np.logical_and(M,currentlyCovered))/(1.0*np.sum(M))<0.5:
      masks.append(M)
      idXs.append(k)
    currentlyCovered = np.logical_or(currentlyCovered,M)

    if len(masks)>9:
      break
  return idXs,masks

def drawBoundariesOverThem(FR,lis):
  MM = FR['image_scaled'].copy()
  for g in lis:
    clr = np.floor(np.random.rand(3)*255)

    gg=sp.ndimage.morphology.binary_erosion(g)
    gg = g-gg
    gg =sp.ndimage.morphology.binary_dilation(gg)
    gg =sp.ndimage.morphology.binary_dilation(gg)
    gg =sp.ndimage.morphology.binary_dilation(gg)
    gg =sp.ndimage.morphology.binary_dilation(gg)

    binary = g*1.0
    for c in range(3):
      MM[gg>0,c] = clr[c]

  plt.imshow(MM)
  plt.show()
def cropImage(InputFrame,masks,black=False):
  """
    given set of masks representing an object, returns the region
    of the image that contains the object
    setting black to true will crop objects with everything else
    blacked out
  """
  img = InputFrame['image_scaled']
  croppedObjs = []
  for mask in masks:
    nonzero_ixs = np.argwhere(mask)
    min_x, max_x = np.min(nonzero_ixs[:,0]), np.max(nonzero_ixs[:,0])
    min_y, max_y = np.min(nonzero_ixs[:,1]), np.max(nonzero_ixs[:,1])
    croppedObjs.append(img[min_x:max_x, min_y:max_y, :])
  return croppedObjs

def feeaturizeVideo(InputVideo):
  """
  Given a modalDB video, it segments each frame and computes the CNN features on pool5 layer
  """
  cn = caffeCNN.CaffeCNN()
  VidFeatures = []
  i=0
  for frame in InputVideo.iter_children(Frame):
    ids,masks = segmentTheFrame(frame)
    croppedProposals = cropImage(frame,masks,black=False)
    Features=cn.featurize_proposals(croppedProposals,ids)
    VidFeatures.append({'name':str(frame),'Features':Features})
    if i>3:
      break
    i+=1
  return VidFeatures

def feeaturizeFrame(InputFrame):
  """
    Given an image, it first segments it and then compute CNN features pretrained on ImageNet
  """
  ids,masks = segmentTheFrame(InputFrame)
  croppedProposals = cropImage(InputFrame,masks,black=False)

  cn = caffeCNN.CaffeCNN()
  Features=cn.featurize_proposals(croppedProposals,ids)
  return Features

def drawThem(FR,lis):
  for g in lis:
    MM = FR['image_scaled'].copy()
    MM[(g*1.0)==0]=0
    plt.imshow(MM)
    plt.show()
