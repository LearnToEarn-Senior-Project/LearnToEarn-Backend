from fastapi import APIRouter, Request

from app.src.object.user.CMUUser.services.CMUUserServices import CMUUserServices

router = APIRouter()


@router.post('/login/{code}')
async def login(code: str):
    return CMUUserServices.getAccessToken(code)


@router.get('/credentials/{token}')
async def getAccessToken(token: str):
    return CMUUserServices.getCredentials(token)


@router.get('/getUser/{id}')
async def getByID(id: str):
    return CMUUserServices.get(id)


@router.post('/addUser')
async def addUser(user: Request):
    return CMUUserServices.add(dict(await user.json())['id'],
                               dict(await user.json())['firstname'],
                               dict(await user.json())['lastname'],
                               dict(await user.json())['email'],
                               dict(await user.json())['role'])


@router.get('/getRole/{id}')
async def getRole(id: str):
    return CMUUserServices.getRole(id)


@router.get('/swapRole/{id}')
async def swapRole(id: str):
    return CMUUserServices.swapRole(id)
