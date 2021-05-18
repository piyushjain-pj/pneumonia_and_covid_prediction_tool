# Importing the necessary libraries
import cv2
import os
import numpy as np
from keras.models import load_model
model_path = r"app/Keras_models_dumps/covid_19_keras_model.h5"
labels = ['COVID', 'NORMAL']
img_size = 150
# load Pretrained model
mymodel = load_model(model_path)


def getPrediction(img):
    N_test = []
    for feature in img:
        N_test.append(feature)
    N_test = np.array(N_test) / 255
    N_test = N_test.reshape(-1, img_size, img_size, 1)
    newsample = N_test
    predictions = mymodel.predict_classes(newsample)
    predictions = predictions.reshape(1, -1)[0]
    return predictions[:1]

def get_input_userdata(dir_add):
    data = []
    try:
        img_arr = cv2.imread(dir_add, cv2.IMREAD_GRAYSCALE)
        # Reshaping images to preferred size
        resized_arr = cv2.resize(img_arr, (img_size, img_size))
        data.append([resized_arr, ])
    except Exception as e:
        print(e)
    img = np.array(data)
    return getPrediction(img)
