from fastapi import APIRouter, Request

from app.src.object.tokenHistory.services.TokenHistoryServices import TokenHistoryServices

router = APIRouter()


@router.post('/addTokenHistory')
async def addTokenTansactionHistory(tokenHistory: Request):
    return TokenHistoryServices.add(dict(await tokenHistory.json())["date"],
                                    float(dict(await tokenHistory.json())["amount"]),
                                    int(dict(await tokenHistory.json())['student_id']),
                                    int(dict(await tokenHistory.json())['reward_id']),
                                   )