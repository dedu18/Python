import cv2
from imutils.object_detection import non_max_suppression
import numpy as np


def personpick(picturepath):
    img = cv2.imread(picturepath)
    orig = img.copy()
    # 定义HOG对象，采用默认参数
    defaultHog = cv2.HOGDescriptor()
    # 设置SVM分类器，用默认分类器
    defaultHog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    # 这里对整张图片进行裁剪
    (rects, weights) = defaultHog.detectMultiScale(img, winStride=(4, 4),padding=(8, 8), scale=1.05)
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    print('检测到人：')
    print(pick)
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(orig, (xA, yA), (xB, yB), (0, 255, 0), 2)
    cv2.imshow("Before NMS", img)
    cv2.imshow("After NMS", orig)
    cv2.waitKey(0)

if __name__ == '__main__':
     personpick("person.jpg")