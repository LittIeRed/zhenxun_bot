import os
from nonebot import on_endswith
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import EventPlainText
from nonebot.rule import to_me
from services.log import logger

from configs.path_config import IMAGE_PATH
from utils.message_builder import image
__zx_plugin_name__ = "角色共鸣"
__plugin_usage__ = """
usage：
    全六星/五星角色共鸣查询
    指令：
        角色名+共鸣
    说明：
        可以只输入角色名简称，以共鸣结尾
    例：
        柏林共鸣
        温妮共鸣
        的士共鸣
""".strip()
__plugin_des__ = "全六星/五星角色共鸣查询"
__plugin_type__ = ("重返未来1999",)
__plugin_version__ = 0.1
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
}

resonance = on_endswith("共鸣", rule=to_me(), priority=5, block=True)

@resonance.handle()
async def _(bot: Bot, event: MessageEvent, arg: str = EventPlainText()):

    if arg.find("共鸣") != -1:
        arg = arg.replace("共鸣", "")
    if not arg:
        await resonance.reject("请输入角色名")

    target_name = arg.upper()
    target_path = IMAGE_PATH / "reverse_1999" / "character_resonance"
    matching_file = None
    for file_name in os.listdir(target_path):
        if target_name in file_name:
            matching_file = file_name
            break

    if matching_file:
        full_file_path = target_path / matching_file
        img = image(full_file_path)
        if img:
            await resonance.finish(img)
        else:
            await resonance.finish("查看角色共鸣信息失败")
    else:
        await resonance.finish("当前还没有该角色的共鸣信息哦")