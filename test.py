import cv2
import numpy as np
import sys
import math

y, u, v = 0, 91, 121
y1, u1, v1 = 138, 156, 161
cnt = 115
pts = []
center = []

im = cv2.imread("to_process/frame115.jpg")
r = cv2.selectROI(im)
cv2.destroyAllWindows()
flag = 0
point = []
in_out = 0
while True:
    img = cv2.imread("to_process/frame{}.jpg".format(cnt))
    w, h, c = img.shape
    roi_shuttle = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    img_hsv = cv2.GaussianBlur(roi_shuttle, (5, 5), 0)
    img_hsv = cv2.cvtColor(img_hsv, cv2.COLOR_BGR2YUV)
    mask = cv2.inRange(
        img_hsv, (np.array([0, u-30, v-30])), (np.array([255, u+30, v+30])))
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    mask_border = cv2.inRange(
        img_hsv, (np.array([y1-30, u1-30, v1-30])), (np.array([y1+30, u1+30, v1+30])))
    border_c, hier = cv2.findContours(mask_border, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
    #border_c = 0
    if len(border_c) > 0:
        bc = max(border_c, key=cv2.contourArea)
        extLeft = tuple(bc[bc[:, :, 0].argmin()][0])
        extRight = tuple(bc[bc[:, :, 0].argmax()][0])
        extTop = list(bc[bc[:, :, 1].argmin()][0])
        extBot = list(bc[bc[:, :, 1].argmax()][0])
        topx = extTop[0] + r[0]
        topy = 0
        botx = extBot[0] + r[0]
        boty = h
        cv2.line(img, (topx, topy), (botx, boty), (255, 120, 200), 3)
        in_out = topx

    if len(contours) > 0:
        (x, y), radius = cv2.minEnclosingCircle(
            max(contours, key=cv2.contourArea))
        if radius > 5:
            cv2.circle(img, (int(x)+r[0], int(y)), 5, (0, 0, 255), -1)
            center = int(x)+r[0], int(y)
        pts.append(center)

    try:
        c = max(contours, key=cv2.contourArea)
    except Exception:
        continue
    (x, y), radius = cv2.minEnclosingCircle(c)
    cv2.circle(img, (int(x)+r[0], int(y)), int(radius), (0, 0, 255), 2)

    for i in range(1, len(pts)-1):
        cv2.line(img, pts[i], pts[i+1], (255, 0, 0), 2)
        if (pts[i][1] - pts[i+1][1]) > 0 and flag == 0:
            point = pts[i]
            flag = 1
        if flag == 1:
            cv2.circle(img, point, 5, (255, 255, 0), -1)

            if list(point)[0] > in_out:
                cv2.putText(img, "IN", (30, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)
            else:
                cv2.putText(img, "OUT", (30, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)

    cv2.imwrite("output_snaps/frame{}.jpg".format(cnt), img)
    cnt += 1
