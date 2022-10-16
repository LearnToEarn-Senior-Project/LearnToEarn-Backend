from fastapi import APIRouter, Request

from app.src.object.token.services.TokenServices import TokenServices

router = APIRouter()


@router.post('/addToken')
async def addToken(add: Request):
    return TokenServices.add(dict(await add.json())['amountOfCoin'])


@router.get('/getAllToken')
async def getTokenAmountOfCoin():
    return TokenServices.getAmountOfCoin()


@router.get('/studentToken/{id}')
async def getStudentToken(id: str):
    return TokenServices.getStudentToken(id)


@router.patch('/sendToken/{course_id}')
async def sendToken(course_id: str):
    return TokenServices.sendToken(course_id)
