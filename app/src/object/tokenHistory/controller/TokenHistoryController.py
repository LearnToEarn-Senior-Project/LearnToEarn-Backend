from fastapi import APIRouter, Request

from app.src.object.tokenHistory.services.TokenHistoryServices import TokenHistoryServices

router = APIRouter()


@router.post('/addTokenHistory/{student_id}/{reward_id}')
async def addTokenTansactionHistory(tokenHistory: Request, student_id: str, reward_id: str):
    return TokenHistoryServices.add(dict(await tokenHistory.json())["date"],
                                    float(dict(await tokenHistory.json())["amount"]),
                                    student_id,
                                    reward_id
                                   )

@router.get('/getAllHistory/{student_id}/page={page}')
async def getAllHistoryBySpecificID(student_id: str, page: int):
    return TokenHistoryServices.getAllTokenHistory(student_id, page)