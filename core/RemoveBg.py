from PIL import Image
from removebg import RemoveBg

api_key = "qFGDzsEgdJnr4mjcsUGucYKA"
file = "car.jpg"
# 填入API-KEY
rmbg = RemoveBg(api_key, "error.log")
# 图片地址
rmbg.remove_background_from_img_file(file)

im = Image.open(file + "_no_bg.png")
x,y = im.size
bule = (67, 142, 219)
red = (255, 0, 0)
write = (255, 255, 255)
tc = write
tc_input = input("请输入照片底色代表字母（B:蓝色，R:红色，W:白色[默认]）:\n")
if tc_input == 'b' or tc_input == 'B':
    print("蓝色\n")
    tc = bule
elif tc_input == 'r' or tc_input == 'R':
    print("蓝色1\n")
    tc = red
else:
    tc = write
try:
  p = Image.new('RGBA', im.size, tc)
  p.paste(im, (0, 0, x, y), im)
  p.save('colored.png')
  print("偷梁换柱！\n")
except:
    print("异常了！\n")