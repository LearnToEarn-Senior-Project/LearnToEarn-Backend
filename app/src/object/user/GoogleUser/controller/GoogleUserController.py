from fastapi import APIRouter, Request

from app.src.object.user.GoogleUser.services.GoogleUserServices import GoogleUserServices

router = APIRouter()


@router.post('/google_login')
async def bindAccount(googleUser: Request):
    return GoogleUserServices.bindAccount(dict(await googleUser.json())['id'],
                                          dict(await googleUser.json())['auth_code'])


@router.post('/google_logout')
async def unbindAccount(googleUser: Request):
    return GoogleUserServices.unbindAccount(dict(await googleUser.json())['id'])


@router.get('/googleGetData/{id}')
async def getData(id: str):
    return GoogleUserServices.get(id)
