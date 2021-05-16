# Importing the necessary libraries
import datetime
import cv2
import os
import numpy as np
from keras.models import load_model

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
labels = ['PNEUMONIA', 'NORMAL']
img_size = 150
##load Pretrained model
print(os.getcwd())
mymodel = load_model("app\Keras_models_dumps\peumonia_keras_model.h5")


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


# Record each inference in a text file


# def recordInferenceEvent(imagePath, outputContent):
#     currentDate = datetime.datetime.now()
#     with open("inference_record.txt", "a") as text_file:
#         text_file.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
#         text_file.write("DATE/TIME : " + str(currentDate.month) + " " + str(currentDate.day) + ", " + str(
#             currentDate.year) + "..." + str(currentDate.hour) + ":" + str(currentDate.minute) + ":" + str(
#             currentDate.second) + "\n\n")
#         text_file.write("IMAGE : " + imagePath + "\n\n")
#         text_file.write("RESULT : " + outputContent + "\n\n\n\n")


# def setXrayImgPath():
#     # copy your image address and paste in input.....
#     imgdir = input("Enter The directory address of image : ")
#     result = get_input_userdata(imgdir)
#     class_label = []
#     if result == 0:
#         class_label.append("Pneumonia")
#         output = "Predicted Class is[0]\nReport Positive Pneumonia Case Found"
#         print("Predicted Class is", result, "\n", class_label, "Detect")
#     else:
#         class_label.append("Normal")
#         output = "Predicted Class is [1]\nReport Negative\nNormal lungs Found"
#         print("Predicted Class is", result, "\n",
#                   class_label, "\nReport Negative")
#         recordInferenceEvent(imgdir, output)

# def setXrayImgPath(imgdir):
#     result = cd.get_input_userdata(imgdir)
#     class_label = []
#     if result == 0:
#         class_label.append("Pneumonia")
#         output = "Predicted Class is[0]\nReport Positive Pneumonia Case Found"
#         print("Predicted Class is", result, "\n", class_label, "Detect")
#     else:
#         class_label.append("Normal")
#         output = "Predicted Class is [1]\nReport Negative\nNormal lungs Found"
#         print("Predicted Class is", result, "\n",
#               class_label, "\nReport Negative")

