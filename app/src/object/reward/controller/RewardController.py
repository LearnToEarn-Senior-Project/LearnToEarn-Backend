from fastapi import APIRouter, Request

from app.src.object.reward.services.RewardServices import RewardServices

router = APIRouter()


@router.get("/rewards/page={page}")
async def getAllPagination(page: int):
    return RewardServices.getAllPagination(page, 10)


@router.get('/reward/{reward_id}')
async def getByID(reward_id: str):
    return RewardServices.getByID(reward_id)


@router.post('/addReward')
async def add(reward: Request):
    return RewardServices.add(dict(await reward.json())["name"],
                              dict(await reward.json())["detail"],
                              dict(await reward.json())['amount'],
                              dict(await reward.json())['price'],
                              dict(await reward.json())['image'])


@router.patch('/updateReward/{reward_id}')
async def adminUpdateReward(reward_id: str, reward: Request):
    return RewardServices.update(reward_id, dict(await reward.json())["name"], dict(await reward.json())["detail"],
                                 dict(await reward.json())["amount"], dict(await reward.json())["price"],
                                 dict(await reward.json())['image'])


@router.delete('/deleteReward/{reward_id}')
async def delete(reward_id: str):
    return RewardServices.delete(reward_id)
