from fastapi import APIRouter, Request

from app.src.object.tokenHistory.services.TokenHistoryServices import TokenHistoryServices

router = APIRouter()


@router.post('/addTokenHistory/{student_id}')
async def addTokenTansactionHistory(tokenHistory: Request, student_id: str):
    return TokenHistoryServices.add(dict(await tokenHistory.json())["date"],
                                    float(dict(await tokenHistory.json())["amount"]),
                                    student_id,
                                    int(dict(await tokenHistory.json())['reward_id']),
                                   )