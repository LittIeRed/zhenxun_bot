import os
from PIL import Image
from configs.path_config import IMAGE_PATH

from io import BytesIO
import base64

def trans_BytesIO(img):
    buf = BytesIO()
    img.markImg.save(buf, format="JPEG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str
def trans_PNG(file_name, img, new_pic):
    #将图片转换为四通道，而第四个通道是我们要修改的透明度，
    #值可以设置成0-255之间的值，透明度会不太一样，看脑洞有多大咯。
    #img = Image.open(initial_pic)
    img = img.convert("RGBA")
    x, y = img.size
    for i in range(x):
        for j in range(y):
            #取四个通道的值，然后用切片取前三个不变，最后一个改为240
            color = img.getpixel((i, j))
            color = color[:-1] + (255,)
            img.putpixel((i, j), color)

    #将白色及近似白色的地方改成半透明
    datas = img.getdata()
    new_data = list()
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(new_pic / f"{file_name}", "PNG")

def rotate_and_save():
    img_path = IMAGE_PATH / "reverse_1999" / "draw_card" / "character"
    img_rotate_path =  IMAGE_PATH / "reverse_1999" / "draw_card" / "character_rotate"
    for file_name in os.listdir(img_path):
        img = Image.open(img_path / f"{file_name}")
        img = img.rotate(-8.5, expand=True)
        trans_PNG(file_name, img, img_rotate_path)

def rotate_and_save_white_png(img:Image):
    img_rotate_path =  IMAGE_PATH / "reverse_1999" / "draw_card" / "character_rotate"
    img = img.rotate(-8.5, expand=True)
    trans_PNG("white.png", img, img_rotate_path)