from nonebot import on_fullmatch
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent, NetworkError, MessageSegment
from nonebot.params import Fullmatch
from utils.message_builder import image
from .draw import draw_one
from .draw import draw_ten
from .utils import rotate_and_save
from services.log import logger
from utils.utils import scheduler
from nonebot import require
require("reverse1999_plugins.draw_card_1999.draw_card_1999_interceptor")
import asyncio



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

# 每日提醒
REMIND_DICK:dict[int, bool] = {}
# USER_NETWORK_ERROR_DICK:dict[int, bool] = {}

@draw.handle()
async def _(event: MessageEvent, msg: str = Fullmatch()):
    # global USER_NETWORK_ERROR_DICK
    global REMIND_DICK
    need_remind = REMIND_DICK.get(event.group_id, True)
    if need_remind:
        await draw.send("使用须知：请在不影响群友正常聊天的情况下使用此功能")
        REMIND_DICK.update({event.group_id: False})
    # has_img_sending = USER_NETWORK_ERROR_DICK.get(event.user_id, False)
    # if has_img_sending:
    #     await draw.finish("别急，上一轮抽卡结果还没出来呢", at_sender=True)
    card_pool = msg[0: 2]
    draw_num = msg[2: 5]
    if "单抽" == draw_num:
        img, current_draw_num = draw_one(event.user_id, card_pool)
        current_draw_num_str = str(current_draw_num)
    else:
        img, current_draw_num = await draw_ten(event.user_id, card_pool)
        current_draw_num_str = str(current_draw_num - 9) + "~" + str(current_draw_num)
    # retry = 3
    # flag = False
    # for i in range(retry):
    #     try:
    if img != "":
        # 这里不走原有工具类image(img)方法，此图片是压缩过后的JPG图片，该方法中会将图片转PNG格式导致图片体积变大
        await draw.send(f"{card_pool}池当前抽数为第{current_draw_num_str}抽" + MessageSegment.image(img), at_sender=True)
            # USER_NETWORK_ERROR_DICK.update({event.user_id:False})
            # flag = True
            # break
    else:
        await draw.finish("角色图片素材丢失", at_sender=True)
        # except NetworkError as e:
        #     # USER_NETWORK_ERROR_DICK.update({event.user_id:True})
        #     logger.error(f"抽卡结果发送网络异常", "抽卡模拟", e=e)
        #     await asyncio.sleep(1)
        # except Exception as e:
        #     logger.error(f"出现未知异常...", "抽卡模拟", e=e)
            # await draw.finish("出现未知异常...", at_sender=True)
    # if not flag:
        # USER_NETWORK_ERROR_DICK.update({event.user_id: False})
        # await draw.finish("网络状况不佳，此次抽卡结果已丢失(私密马赛", at_sender=True)

rotate = on_command("旋转", priority=5, block=True)

# 重置凌晨提醒
@scheduler.scheduled_job(
   "cron",
   hour=0,
   minute=0,
)
async def _():
    global REMIND_DICK
    REMIND_DICK.clear()

# 重置午间提醒
@scheduler.scheduled_job(
   "cron",
   hour=12,
   minute=0,
)
async def _():
    global REMIND_DICK
    REMIND_DICK.clear()


@rotate.handle()
async def _(bot: Bot, event: MessageEvent):
    # 判断是否是超级用户
    if str(event.user_id) in bot.config.superusers:
        rotate_and_save()
        await rotate.finish("旋转完成")
