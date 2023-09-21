import os
import random
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, MessageSegment
from nonebot.matcher import Matcher
from .random_voice import voice


__zx_plugin_name__ = "戳一戳掉落语音"

__plugin_usage__ = """
usage：
    戳一戳-1999全角色语音随机掉落
    cd: 60s
""".strip()
__plugin_des__ = "戳一戳-1999全角色语音随机掉落"
__plugin_type__ = ("重返未来1999",)
__plugin_version__ = 0.1
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
}

poke_ = on_notice(priority=4, block=True)

@poke_.handle()
async def _(event: PokeNotifyEvent):
    voice_record, img = await voice()
    await poke_.send(voice_record)
    await poke_.finish(MessageSegment.image(img))
