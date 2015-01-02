####################
# Class: CaffeCNN
# ---------------
# contains everything needed to apply a Caffe CNN
# to images in order to get feature representations
####################
import os
import numpy as np
import scipy as sp
import caffe


class CaffeCNN:

	def __init__(self):
		"""
			loads the network
		"""
		if not 'CAFFE_ROOT_PATH' in os.environ.keys():
			raise Exception("Run configure.sh to set environmental variables! Caffe not found")
		self.caffe_root = os.environ['CAFFE_ROOT_PATH']
		self.deploy_prototxt_path = os.path.join(self.caffe_root, 'models/bvlc_reference_caffenet/deploy.prototxt')
		self.model_path = os.path.join(self.caffe_root, 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel')
		self._cnn = None


	@property
	def cnn(self):
		"""
			property representing the net itself
			Allows us to lazily load it.
		"""
		if self._cnn is None:
			self._cnn = caffe.Classifier(self.deploy_prototxt_path, self.model_path)
			self._cnn.set_phase_test()
			self._cnn.set_raw_scale('data', 255) #operates on 0-255 scale, not 0-1
		return self._cnn


	def featurize(self, image):
		"""
			given an image, returns a feature vector representing the top-level
			activations of this network
		"""
		self.cnn.predict([image])
		return self.cnn.blobs['pool5'].data[4].flatten()


	def featurize_frame(self, frame, n=50, black=False):
		"""
			given a frame, returns a mapping:
				features: mask_ix -> feature_array
		"""
		proposals = frame.top_n_cropped_object_proposals(n=25, black=False)
		return {ix:self.featurize(obj) for ix, obj in proposals}

	def featurize_proposals(self, proposals,ids):
		"""
			given a frame, returns a mapping:
				features: mask_ix -> feature_array
		"""
		return {ids[ix]:self.featurize(obj) for ix, obj in enumerate(proposals)}
