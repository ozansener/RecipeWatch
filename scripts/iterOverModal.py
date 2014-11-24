from scipy.io import loadmat, savemat
from scipy.misc import imread, imsave
import cPickle
import subprocess
import re
import glob

import matplotlib.pyplot as plt

from ModalDB import * # if you get an import error here, shut down ipython notebook and run the configuration script.
from Settings import Settings

modaldb_client = ModalClient(root=Settings.data_dir, schema=Settings.my_schema) # here, we specify the DB's location (on disk) and schema.


for video in modaldb_client.iter(Video):
  frame=video.get_random_child()
  plt.imshow(frame['image_scaled'])
  plt.show()
