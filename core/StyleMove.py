import cv2
import glob


def style_move(model_type = 0, picture_path = ''):
    # 加载模型
    net = cv2.dnn.readNetFromTorch(models[model_type])
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
    # 读取图片
    image = cv2.imread(picture_path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
    # 进行计算
    net.setInput(blob)
    out = net.forward()
    out = out.reshape(3, out.shape[2], out.shape[3])
    out[0] += 103.939
    out[1] += 116.779
    out[2] += 123.68
    out /= 255
    out = out.transpose(1, 2, 0)
    # 输出图片
    cv2.imshow('Style Moved Picture', out)
    # cv2.imwrite('./StyledImage.jpg', out)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    file_path = '../picture3.png'
    models = glob.glob('./models/*/*.t7')
    print(models)
    print("一共有%d种模型" % len(models))
    while True:
        model_type = input("请输入要迁移的风格：")
        if (-1 == int(model_type)):
            break
        style_move(int(model_type), file_path)
