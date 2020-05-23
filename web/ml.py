import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from PIL import Image
import numpy as np

image_generator = ImageDataGenerator(rescale=1./255)
model = tf.keras.models.load_model('./flaskr/static/ml/my_model.h5')
PATH = os.path.join('./flaskr/static/assets','image.jpg')

IMG_HEIGHT = 150
IMG_WIDTH = 150

def check_photo():

    img = tf.io.read_file(PATH)
    img=decode_img(img)
    evaluate(img)
    # model.summary()


def evaluate(img):
    img = (np.expand_dims(img,0))
    preds = model.predict(img)
    print(preds)

def decode_img(img):
    img = tf.image.decode_jpeg(img,channels=3) #color images
    img = tf.image.convert_image_dtype(img, tf.float32) 
    #convert unit8 tensor to floats in the [0,1]range
    return tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT]) 