"""
Extracts features from tracklets.
Uses Oxford VGG-face: github.com/rcmalli/keras-vggface
VGGFace(model='') can handle vgg16, resnet50, or senet50
"""

import numpy as np
from keras.preprocessing import image
from keras_vggface.vggface import VGGFace
from keras_vggface import utils
from keras.engine import Model
from os import listdir
import tensorflow as tf

class KeypointExtractor:

    def __init__(self):
        layer_name = 'flatten_1'
        vgg_model = VGGFace(model='resnet50')
        out = vgg_model.get_layer(layer_name).output
        self.vgg_model_fc7 = Model(vgg_model.input, out)
        tf.logging.set_verbosity(tf.logging.ERROR)

    # returns list of shape (1, 4096)
    def getFeaturesFromFile(self, path):
        # Load image
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = utils.preprocess_input(x, version=1)  # or version=2

        fc7_output = self.vgg_model_fc7.predict(x)

        # return normalized output
        return fc7_output/(np.linalg.norm(fc7_output))

    def getAllFeatures(self, tracklet, image_dir):
        keypoints = []
        tracklet_id = "".join(str(x) for x in tracklet.color)

        for image in listdir(image_dir+"/"+tracklet_id+"/"):
            path = image_dir+"/"+tracklet_id+"/"+image
            keypoints.append(self.getFeaturesFromFile(path))

        return keypoints