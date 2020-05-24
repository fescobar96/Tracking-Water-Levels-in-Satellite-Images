import os
from os.path import join
from os.path import dirname
from os.path import realpath
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Input
from tensorflow.keras.layers import Conv2D 
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Conv2DTranspose
from tensorflow.keras.layers import concatenate
from tensorflow.keras import Model
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import matplotlib

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/') # where uploaded files are stored

# Dice Loss Function
def dice_loss(y_true, y_pred):
  loss = 1 - dice_coeff(y_true, y_pred)
  return loss

# BCE Dice Loss Function
def bce_dice_loss(y_true, y_pred):
  loss = tf.keras.losses.binary_crossentropy(y_true, y_pred) + dice_loss(y_true, y_pred)
  return loss

# Load Model
model = load_model('static/model/satellite_unet.hdf5', custom_objects={'dice_loss':dice_loss, 'bce_dice_loss':bce_dice_loss})

# Create mask
def generate_mask(image_url):
	image = load_img(image_url, target_size=(128, 128))
	image = img_to_array(image)/255.0
	image = np.expand_dims(image, axis=0)
	mask = model.predict(image)
	return mask
# Calculate water percentage
def calculate_water(predicted_mask):
	white = len(predicted_mask[predicted_mask>=0.5])
	black = len(predicted_mask[predicted_mask<0.5])
	water_percentage = white / (white+black)
	return water_percentage

#post image
def post_image(image_url):
    image = open(image_url, 'rb').read()
    response = requests.post(URL, data=img, headers=headers)
    return response

# Control Workflow of Server.py
def workflow(image_url):
	mask = generate_mask(image_url)
	mask = np.squeeze(mask, axis=0)
	water_percentage = calculate_water(mask)
	land_percentage = 100 - water_percentage
	matplotlib.image.imsave(os.path.join(UPLOAD_FOLDER, 'mask.png'), mask)

	image = Image.open(os.path.join(UPLOAD_FOLDER, 'mask.png'))
	image = image.convert('1')
	image = img_to_array(image)
	water_percentage = round(calculate_water(image)*100,2)
	land_percentage = round(100 - water_percentage,2)
	results = {	'mask': mask,
				'water_percentage': str(water_percentage) + '%', 
				'land_percentage':str(land_percentage) + '%'}
	return results