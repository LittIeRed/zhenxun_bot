import os
import random
import json

from configs.path_config import RECORD_PATH
from services.log import logger
from utils.message_builder import image, record
from utils.utils import CountLimiter, is_chinese
from utils.image_utils import text2image
from PIL import Image
from utils.image_utils import BuildImage

from io import BytesIO
import base64


async def voice():
    # 随机抽取语音
    voice_record, encontent, content = random_voice()

    # 处理语音文本
    # new_en_str, new_ch_str, en_font_size, ch_font_size, en_add_height = process_text(encontent, content)

    # 构建语音对象及文本图片
    new_image = await build_result(encontent, content)

    #返回结果
    return voice_record, trans_BytesIO(new_image)

def trans_BytesIO(img):
    buf = BytesIO()
    img.markImg.save(buf, format="JPEG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str

def random_voice():
    # 随机获取语音
    voice_path = RECORD_PATH / "reverse_1999" / "character_voice" / "voice"
    character_name = random.choices(os.listdir(voice_path), k=1)[0]
    voice_name = random.choices(os.listdir(voice_path / character_name), k=1)[0]
    voice_record = record(voice_path / character_name / voice_name)

    # 获取语音对应文本
    voice_detail_name = str(voice_name).split(".")[0].split("_")[1]
    text_path = RECORD_PATH / "reverse_1999" / "character_voice" / "json" / (character_name + ".json")
    with open(text_path, 'r', encoding='utf-8') as file:
        # 读取文件内容并解析为 JSON
        data = json.load(file)
        encontent = data[voice_detail_name]["encontent"]
        content = data[voice_detail_name]["content"]
    return voice_record, encontent, content

def process_text(encontent, content):
    new_en_str = encontent
    new_ch_str = content
    if len(encontent) <= 150:
        new_en_str = en_line_break(encontent, 50)
        en_font_size = 45
        en_add_height = 55
    else:
        new_en_str = en_line_break(encontent, 60)
        en_font_size = 45
        en_add_height = 55

    if len(content) <= 25:
        ch_font_size = 45
    else:
        new_ch_str = ch_line_break(content, 25)
        ch_font_size = 45
    return new_en_str, new_ch_str, en_font_size, ch_font_size, en_add_height

async def build_result(encontent, content):
    en_img = await text2image(
        text=encontent,
        font="AGENCYB.TTF",
        font_size=45,
        font_color="white",
        auto_parse=False,
        padding=10,
        _add_height=55, # 处理文字下划线的bug，其实是背景没有完全透明，height高度太低
        is_alpha=True,
        color="white",
    )
    ch_img = await text2image(
        text=content,
        font_size=50,
        font_color="white",
        auto_parse=False,
        padding=10,
        _add_height=60,
        is_alpha=True,
        color="white",
    )
    new_height = en_img.h + ch_img.h + 30
    new_wight = (en_img.w if en_img.w > ch_img.w else ch_img.w) + 30
    new_image = BuildImage(w=new_wight, h=new_height, background=RECORD_PATH / "reverse_1999" / "character_voice" / "语音背景.jpg")
    await new_image.apaste(img=en_img, pos=(10, 25), alpha=True)
    await new_image.apaste(img=ch_img, pos=(10, en_img.h + 20), alpha=True)
    return new_image

def en_line_break(en_str, space_step):
    new_en_str = ""
    start_space_index = 0
    end_space_index = start_space_index + space_step
    while True:
        # 固定切换长度(对应end切片坐标)再往后找到第一个" "空格作为新的分片长度
        temp_space_index = en_str.find(" ", end_space_index)
        if temp_space_index != -1:
            end_space_index = temp_space_index
            substring = en_str[start_space_index:end_space_index]
            new_en_str += substring + "\n"
            start_space_index = end_space_index
            end_space_index = start_space_index + space_step
        else:
            substring = en_str[start_space_index:]
            new_en_str += substring
            break
    return new_en_str

def ch_line_break(ch_str, space_step):
    new_ch_str = ""
    start_space_index = 0
    end_space_index = start_space_index + space_step
    while True:
        substring = ch_str[start_space_index:end_space_index]
        if len(substring) < end_space_index - start_space_index:
            new_ch_str += substring
            break
        else:
            # 判断是否是中文，确保不会把英文单词截成两半，注意end_space_index-1
            if not ('\u4e00' <= str(ch_str)[end_space_index-1] <= '\u9fff'):
                end_space_index += 1
                continue
            new_ch_str += substring + "\n"
            start_space_index = end_space_index
            end_space_index = start_space_index + space_step
    return new_ch_str
