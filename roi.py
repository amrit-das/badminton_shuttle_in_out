import cv2
import numpy as np
import sys

im = cv2.imread(sys.argv[1])
r = cv2.selectROI(im)
#print(r)
imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
cv2.imshow("Image", imCrop)
cv2.waitKey(0)

