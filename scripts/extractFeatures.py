#import numpy as np
#import scipy as sp

from RecipeVision import caffeCNN
from scipy.misc import imread, imsave

A = imread('im.png')

cn = caffeCNN.CaffeCNN()
B=cn.featurize(A)
