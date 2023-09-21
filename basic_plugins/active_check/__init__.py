from nonebot import on_message
from nonebot.params import EventPlainText
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP
from services.log import logger
from utils.utils import scheduler
import asyncio



__zx_plugin_name__ = "活跃检测 [Hidden]"


__plugin_usage__ = """
""".strip()
__plugin_version__ = 0.1
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
}

active_check = on_message(
    # 响应优先级，用于指定响应器的优先级。响应器的优先级越小，越先被触发。如果响应器的优先级相同，则按照响应器的注册顺序进行触发。
    priority=999,
    # 用于指定响应器是否阻断事件的传播。如果阻断为 True，则在该响应器被触发后，事件将不会再传播给其他下一优先级的响应器。
    block=False,
    permission=GROUP,
)

ACTIVE_CHECK_DICT:dict[str, int] = {}


"""
setter方法
.setdefault()：如果键不存在，添加默认值，并返回默认值，
    如果键 key 存在，.不会修改已有的键值对，只是返回键 key 对应的值。
.update()：用于合并或更新字典，不返回值，只是更新当前字典;
    如果键不存在，不会引发错误，而是会添加新的键值对到字典中
getter方法
group_data['group1']['member1']：直接使用键来访问字典中的值，
    如果键不存在，它可能引发 KeyError 异常。
.get(key, default)：如果键存在，则返回该键的值；如果键不存在，则返回指定的 default 值，
    如果没有提供 default 值，则返回 None。
"""

@active_check.handle()
async def _(event: GroupMessageEvent):
    global ACTIVE_CHECK_DICT
    key = str(event.group_id) + "_" + str(event.user_id)
    message_count = ACTIVE_CHECK_DICT.get(key, 0)
    ACTIVE_CHECK_DICT.update({key: message_count + 1})

def is_pass_active_check(group_id:int, user_id:int, request_count: int):
    global ACTIVE_CHECK_DICT
    key = str(group_id) + "_" + str(user_id)
    message_count = ACTIVE_CHECK_DICT.get(key, 0)
    return message_count and message_count >= request_count


# 凌晨重置
@scheduler.scheduled_job(
   "cron",
   hour=6,
   minute=0,
)
async def _():
    global ACTIVE_CHECK_DICT
    ACTIVE_CHECK_DICT.clear()
