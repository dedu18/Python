import cv2
import time

# 读入一个图片
img = cv2.imread("ocr.jpg", cv2.IMREAD_COLOR)
print(type(img))
# # 在窗口显示图片
# cv2.imshow('图片标题', img)

# 边缘检测
cv2.imwrite("canny.jpg", cv2.Canny(img, 200, 300))
cv2.imshow("canny.jpg", cv2.imread("canny.jpg", cv2.IMREAD_COLOR))

while True:
    # 获取键盘输入，可使用cv2.setMouseCallback()获取鼠标操作
    key = cv2.waitKey(0)
    if key == 27:
        # 释放有OpenCV创建的所有窗口
        cv2.destroyAllWindows()
    else:
        print("ESC 退出")
    time.sleep(5)




