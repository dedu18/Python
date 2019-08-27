import cv2


# 定义方法 基于haar特征级联进行人脸检测
def detect(file):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    print(type(face_cascade))
    img = cv2.imread(file)
    print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print("检测到了人脸")
    print(faces)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.namedWindow("改变了")
    cv2.imshow("改变了2", img)
    cv2.imwrite('./test.jpg', img)
    cv2.waitKey(0)

file_name = 'aobama-1.jpg'
detect(file_name)



