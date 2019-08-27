# 构建人脸特征向量库
import dlib
import numpy as np
import cv2
import os
import json

# 基于dlib中提供的人脸检测方法（使用HOG特征或卷积神经网方法），并使用提供的深度残差网络（ResNet）实现实时人脸识别

# 图像的目录
imagePath = '../../images/'
# 定义一个128维的空向量data
data = np.zeros((1, 128))
#定义空的list存放人脸的标签
label = []
# 传统的HOG特征+级联分类的方法，效果没有CNN好
# detector = dlib.get_frontal_face_detector()
# # 使用的是CNN进行人脸检测，如果你没有GPU，或者你有GPU但没有进行GPU的配置，那么速度很慢
# # detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
# sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

for file in os.listdir(imagePath):
    if '.jpg' in file or '.png' in file:
        label = file.split('-')[0]
        print("目前的图片", file)
        print("标签", label)