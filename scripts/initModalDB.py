from ModalDB import *
from scipy.io import loadmat, savemat
from scipy.misc import imread, imsave
import pysrt
import cPickle

from Settings import Settings

import os
modaldb_client = ModalClient(root=Settings.data_dir, schema=Settings.my_schema) # here, we specify the DB's location (on disk) and schema.
modaldb_client.clear_db() # empty the database just in case.
