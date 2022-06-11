from fastapi import APIRouter, Request

from app.src.object.token.services.TokenServices import TokenServices

router = APIRouter()


@router.post('/addToken')
async def addToken(add: Request):
    return TokenServices.addToken(dict(await add.json())['amount'])


@router.get('/getAllToken')
async def getTokenAmount():
    return TokenServices.getTokenAmount()


@router.get('/studentToken/{id}')
async def getStudentToken(id: str):
    return TokenServices.getStudentToken(id)
