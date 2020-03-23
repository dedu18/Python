# 二维码模块
# 生成二维码 pip install qrcode
# 解析二维码 pip install pyzbar

import cv2
import qrcode
from pyzbar.pyzbar import decode

# 转GBK编码
def zh_ch_gbk(string):
    return string.encode("gbk").decode(errors="ignore")

image_maked = qrcode.make("你好, 我ssss")
image_maked.save('qrcode.png')
image_read = cv2.imread('erweima.png')
barcodes = decode(image_read)
# 循环检测到的条形码
for barcode in barcodes:
    # 提取条形码的边界框的位置
    # 画出图像中条形码的边界框
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image_read, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 条形码数据为字节对象，所以如果我们想在输出图像上
    # 画出来，就需要先将它转换成字符串
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # 绘出图像上条形码的数据和条形码类型
    # text = "{} ({})".format(barcodeData, barcodeType)
    text = "{}".format(barcodeData)
    cv2.putText(image_read, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
     0.5, (0, 0, 255), 2)

    # 向终端打印条形码数据和条形码类型
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    # 展示输出图像
    cv2.imshow(zh_ch_gbk("扫描二维码"), image_read)
    cv2.waitKey(0)

