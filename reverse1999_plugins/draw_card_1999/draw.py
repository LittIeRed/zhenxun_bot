from utils.image_utils import BuildImage
from .model import UpEvent, PSEUDO_LIMITED_CARDPOOL, ROTATE_UP_CARDPOOL
from .up_draw import draw_one as up_draw_one, draw_ten as up_draw_ten
from .not_up_draw import draw_one as not_up_draw_one, draw_ten as not_up_draw_ten

UP_CARDPOOL_DICK: dict[str, list[UpEvent]] = {
    '限定': PSEUDO_LIMITED_CARDPOOL,
    '轮换': ROTATE_UP_CARDPOOL
}
def draw_one(user_id: int, card_pool_name: str):
    card_pool = UP_CARDPOOL_DICK.get(card_pool_name)
    if card_pool:
        return up_draw_one(user_id, card_pool)
    else:
        return not_up_draw_one(user_id)

async def draw_ten(user_id: int, card_pool_name: str):
    card_pool = UP_CARDPOOL_DICK.get(card_pool_name)
    if card_pool:
        return await up_draw_ten(user_id, card_pool)
    else:
        return await not_up_draw_ten(user_id)


__all__ = [
    'draw_one',
    'draw_ten'
]
