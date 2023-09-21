import random
from configs.path_config import IMAGE_PATH
from utils.image_utils import BuildImage
from PIL import Image
from .model import PERMANENT_CARDPOOL
from .utils import rotate_and_save_white_png, trans_BytesIO

# 常驻池各星级角色保底计数
USERS_COUNT_FOR_SIX: dict[int, int] = {}
USERS_COUNT_FOR_FIVE: dict[int, int] = {}
USERS_COUNT_FOR_FOUR: dict[int, int] = {}

# 常驻池单抽
def draw_one(draw_seed: int):
    # 获取抽卡前抽数再 + 1
    draw_count_for_six = USERS_COUNT_FOR_SIX.get(draw_seed, 0) + 10
    character_name = draw_one_operator(draw_seed)
    img_path = IMAGE_PATH / "reverse_1999" / "draw_card" / "character" / f"{character_name}.png"
    if img_path.exists():
        return img_path, draw_count_for_six
    else:
        return "", draw_count_for_six

# 常驻池十连
async def draw_ten(draw_seed: int):
    img = build_background_img()
    pos_list = [(338, -100), (577, 35), (845, -31), (1083, 105), (1352, 38),
                (260, 442), (499, 577), (767, 511), (1005, 647), (1274, 580)]

    # 获取抽卡前抽数再 + 10
    draw_count_for_six = USERS_COUNT_FOR_SIX.get(draw_seed, 0) + 10

    for i in range(len(pos_list)):
        character_name = draw_one_operator(draw_seed)
        img_path = IMAGE_PATH / "reverse_1999" / "draw_card" / "character_rotate" / f"{character_name}.png"
        if img_path.exists():
            paste_img = Image.open(img_path)
        else:
            print("这张图片不见了", img_path)
            img_path = IMAGE_PATH / "reverse_1999" / "draw_card" / "character_rotate" / "white.png"
            if img_path.exists():
                paste_img = Image.open(img_path)
            else:
                rotate_and_save_white_png(Image.new("RGB", (250, 455), (255, 255, 255)))
                paste_img = Image.open(img_path)
        await img.apaste(img=paste_img, pos=pos_list.pop(0), alpha=True)
    # 这里不走原有工具类image(img)方法，此图片是压缩过后的JPG图片，该方法中会将图片转PNG格式导致图片体积变大
    img = trans_BytesIO(img)
    return img, draw_count_for_six

def build_background_img():
    img_path = IMAGE_PATH / "reverse_1999" / "draw_card" / "background" / "draw_bg.jpg"
    if img_path.exists():
        return BuildImage(w=0, h=0, background=(IMAGE_PATH / "reverse_1999" / "draw_card" / "background" / "draw_bg.jpg"))
    else:
        return BuildImage(w=1920, h=1080),


def draw_one_operator(user_id: int) -> str:
    star = confirm_star(user_id)
    character_name = random.choices(
        [x.name for x in PERMANENT_CARDPOOL if (
                x.star == star and not any([x.is_limited]))],
        k=1)[0]
    return character_name

def confirm_star(user_id):
    global USERS_COUNT_FOR_SIX
    global USERS_COUNT_FOR_FIVE
    global USERS_COUNT_FOR_FOUR
    draw_count_for_six = USERS_COUNT_FOR_SIX.get(user_id, 0) + 1
    draw_count_for_five = USERS_COUNT_FOR_FIVE.get(user_id, 0) + 1
    draw_count_for_four = USERS_COUNT_FOR_FOUR.get(user_id, 0) + 1
    USERS_COUNT_FOR_SIX.update({user_id: draw_count_for_six})
    USERS_COUNT_FOR_FIVE.update({user_id: draw_count_for_five})
    USERS_COUNT_FOR_FOUR.update({user_id: draw_count_for_four})
    # 首先要先决定出的星级
    if 0 <= draw_count_for_six <= 60:
        # 没有抽过或者刚刚重置过, 无概率提升
        star = random.choices([6, 5, 4, 3, 2], weights=[1.5, 8.5, 40, 45, 5], k=1)[0]
    elif 60 < draw_count_for_six <= 69:
        # 触发概率提升
        if random.randint(1, 100) <= 4 + (draw_count_for_six - 61) * 2.5:
            # 触发概率提升则为6星
            star = 6
        else:
            # 否则则在5, 4, 3, 2星中随机
            star = random.choices([5, 4, 3, 2], weights=[8.5, 40, 45, 5], k=1)[0]
    else:
        # 70抽保底
        star = 6
    # 保底触发升级
    # 每10抽必出4星及以上
    if star <= 4 and draw_count_for_four > 0 and draw_count_for_four % 10 == 0:
        star = 4
    # 每20抽必出5星或6星
    if star <= 5 and draw_count_for_five > 0 and draw_count_for_five % 20 == 0:
        star = 5
    # 如果出4星则重置4星保底计数
    if star == 4:
        USERS_COUNT_FOR_FOUR.update({user_id: 0})
    # 如果出5星则重置5星、4星保底计数
    if star == 5:
        USERS_COUNT_FOR_FOUR.update({user_id: 0})
        USERS_COUNT_FOR_FIVE.update({user_id: 0})
    # 如果出6星则重置5星、6星、4星保底计数
    if star == 6:
        USERS_COUNT_FOR_FOUR.update({user_id: 0})
        USERS_COUNT_FOR_FIVE.update({user_id: 0})
        USERS_COUNT_FOR_SIX.update({user_id: 0})
    return star
