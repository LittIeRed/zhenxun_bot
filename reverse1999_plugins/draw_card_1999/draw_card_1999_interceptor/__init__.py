from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent, GROUP, NetworkError
from nonebot.matcher import Matcher
#from basic_plugins.active_check import is_pass_active_check
from nonebot import require
require("active_check")
from basic_plugins.active_check import is_pass_active_check
from utils.manager import plugins2count_manager


__zx_plugin_name__ = "抽卡模拟拦截器[Hidden]"
__plugin_usage__ = """
""".strip()
__plugin_version__ = 0.1
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
}
draw_interceptor = on_fullmatch(msg=("常驻十连", "轮换十连", "限定十连", "常驻单抽", "轮换单抽", "限定单抽"), priority=4, permission=GROUP, block=False)
@draw_interceptor.handle()
async def _(matcher: Matcher, event: GroupMessageEvent):
    if plugins2count_manager.check("draw_card_1999", event.group_id):
        if not is_pass_active_check(event.group_id, event.user_id, 3):
            matcher.stop_propagation()
            await draw_interceptor.finish("先聊会儿天吧~", at_sender=True)

