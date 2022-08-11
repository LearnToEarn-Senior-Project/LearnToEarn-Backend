from fastapi import APIRouter, Request
from app.src.server.database import DB
from app.src.object.reward.services.RewardServices import RewardServices

router = APIRouter()


@router.get("/rewards/page={page}")
async def getAllPagination(page: int):
    return RewardServices.getAllPagination(page)


@router.get('/reward/{reward_id}')
async def getByID(reward_id: str):
    return RewardServices.getByID(reward_id)


@router.post('/addReward')
async def add(reward: Request):
    try:
        image_url = dict(await reward.json())['image']
    except:
        image_url = None
    return RewardServices.add(dict(await reward.json())["name"],
                              dict(await reward.json())["detail"],
                              int(dict(await reward.json())['amount']),
                              float(dict(await reward.json())['price']),
                              image_url)


@router.patch('/updateReward/{reward_id}')
async def adminUpdateReward(reward_id: str, reward: Request):
    try:
        image_url = dict(await reward.json())['image']
    except:
        image_url = list(DB.DATABASE['reward'].find({"_id": reward_id}).limit(1))[0]["image"]
    return RewardServices.update(reward_id,
                                 dict(await reward.json())["name"],
                                 dict(await reward.json())["detail"],
                                 dict(await reward.json())["amount"],
                                 dict(await reward.json())["price"],
                                 image_url)


@router.delete('/deleteReward/{reward_id}')
async def delete(reward_id: str):
    return RewardServices.delete(reward_id)


@router.patch('/buyReward/{user_id}')
async def buy(reward: Request, user_id: str):
    return RewardServices.buy(dict(await reward.json())["_id"],
                              user_id)
