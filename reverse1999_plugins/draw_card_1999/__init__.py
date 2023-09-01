import os
from nonebot import on_fullmatch
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import EventPlainText
from nonebot.params import Fullmatch
from utils.message_builder import image
from .draw import draw_one
from .draw import draw_ten
from .utils import rotate_and_save


__zx_plugin_name__ = "抽卡模拟"
__plugin_usage__ = """
usage：
    1999抽卡模拟
    本抽卡模拟会尽量还原1999本身的抽卡机制及各星级角色抽取概率
    目前有三个卡池：常驻、轮换、限定
    指令：
        卡池+十连/单抽
    示例:
        常驻十连  常驻单抽
        轮换十连  轮换单抽
        限定十连  限定单抽
    抽卡CD：10s
""".strip()
__plugin_des__ = "抽卡模拟"
__plugin_type__ = ("重返未来1999",)
__plugin_version__ = 0.1
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
}

draw = on_fullmatch(msg=("常驻十连", "轮换十连", "限定十连", "常驻单抽", "轮换单抽", "限定单抽"), priority=5, block=True)


@draw.handle()
async def _(bot: Bot, event: MessageEvent, msg: str = Fullmatch()):
    card_pool = msg[0: 2]
    draw_num = msg[2: 5]
    if "单抽" == draw_num:
        img, current_draw_num = draw_one(event.user_id, card_pool)
    else:
        img, current_draw_num = draw_ten(event.user_id, card_pool)
    if img != "":
        await draw.finish(card_pool + "池当前抽数为第"+ str(current_draw_num - 9) + "~" + str(current_draw_num) +"抽" + image(img), at_sender=True)
    else:
        await draw.finish("角色图片素材丢失", at_sender=True)
