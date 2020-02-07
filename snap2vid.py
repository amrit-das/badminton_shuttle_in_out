import cv2
import numpy as np
import os,sys

img_array = []
files = os.listdir("output_snaps/")
filed = []
for idx,_ in enumerate(files):
    try:
        img = cv2.imread("video_snaps/frame{}.jpg".format(idx))
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        print(idx)
    except:
        print(idx,"Error")
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
