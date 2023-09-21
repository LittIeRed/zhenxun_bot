from pydantic import BaseModel

class Operator(BaseModel):
    name: str
    star: int
    is_limited: bool  # 限定

class UpEvent(BaseModel):
    star: int  # 对应up星级
    operator: list[Operator]  # 角色列表
    zoom: float  # up提升倍率


# 伪限定池
PSEUDO_LIMITED_CARDPOOL: list[UpEvent] = [
    UpEvent(
        star=6,
        operator=[
            Operator(name='鬃毛沙砾', star=6, is_limited=True),
        ],
        zoom=0.5
    ),
    UpEvent(
        star=5,
        operator=[
            Operator(name='坎吉拉', star=5, is_limited=True),
            Operator(name='坦南特', star=5, is_limited=False),
        ],
        zoom=0.5
    )
]

# 常驻轮换
ROTATE_UP_CARDPOOL: list[UpEvent] = [
    UpEvent(
        star=6,
        operator=[
            Operator(name='温妮弗雷德', star=6, is_limited=False),
        ],
        zoom=0.5
    ),
    UpEvent(
        star=5,
        operator=[
            Operator(name='婴儿蓝', star=5, is_limited=False),
            Operator(name='咔嚓咔嚓', star=5, is_limited=False),
        ],
        zoom=0.5
    )
]


# 常驻池
PERMANENT_CARDPOOL: list[Operator] = [
    Operator(name='槲寄生', star=6, is_limited=False),
    Operator(name='红弩箭', star=6, is_limited=False),
    Operator(name='未锈铠', star=6, is_limited=False),
    Operator(name='苏芙比', star=6, is_limited=False),
    Operator(name='星锑', star=6, is_limited=False),
    Operator(name='百夫长', star=6, is_limited=False),
    Operator(name='泥鯭的士', star=6, is_limited=False),
    Operator(name='兔毛手袋', star=6, is_limited=False),
    Operator(name='远旅', star=6, is_limited=False),
    Operator(name='温妮弗雷德', star=6, is_limited=False),
    Operator(name='新巴别塔', star=6, is_limited=False),
    Operator(name='X', star=5, is_limited=False),
    Operator(name='玛丽莲', star=5, is_limited=False),
    Operator(name='婴儿蓝', star=5, is_limited=False),
    Operator(name='夏利', star=5, is_limited=False),
    Operator(name='柏林以东', star=5, is_limited=False),
    Operator(name='帕米埃', star=5, is_limited=False),
    Operator(name='气球派对', star=5, is_limited=False),
    Operator(name='讣告人', star=5, is_limited=False),
    Operator(name='五色月', star=5, is_limited=False),
    Operator(name='坦南特', star=5, is_limited=False),
    Operator(name='喀嚓喀嚓', star=5, is_limited=False),
    Operator(name='尼克·波顿', star=4, is_limited=False),
    Operator(name='小春雀儿', star=4, is_limited=False),
    Operator(name='冬', star=4, is_limited=False),
    Operator(name='芭妮芭妮', star=4, is_limited=False),
    Operator(name='狼群', star=4, is_limited=False),
    Operator(name='雾行者', star=4, is_limited=False),
    Operator(name='红斗篷', star=4, is_limited=False),
    Operator(name='APPLe', star=4, is_limited=False),
    Operator(name='铅玻璃', star=4, is_limited=False),
    Operator(name='TTT', star=4, is_limited=False),
    Operator(name='爱宠', star=4, is_limited=False),
    Operator(name='莫桑女士', star=4, is_limited=False),
    Operator(name='吵闹鬼', star=4, is_limited=False),
    Operator(name='小梅斯梅尔', star=4, is_limited=False),
    Operator(name='埃里克', star=4, is_limited=False),
    Operator(name='弄臣', star=3, is_limited=False),
    Operator(name='拉拉泉', star=3, is_limited=False),
    Operator(name='星之眼', star=3, is_limited=False),
    Operator(name='莉拉妮', star=3, is_limited=False),
    Operator(name='约翰·提托', star=3, is_limited=False),
    Operator(name='丽莎&路易斯', star=3, is_limited=False),
    Operator(name='贝蒂', star=3, is_limited=False),
    Operator(name='哒哒达利', star=3, is_limited=False),
    Operator(name='洋葱头', star=3, is_limited=False),
    Operator(name='斯普特尼克', star=3, is_limited=False),
    Operator(name='无线电小姐', star=2, is_limited=False),
    Operator(name='门', star=2, is_limited=False),
]