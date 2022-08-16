from fastapi import APIRouter, UploadFile, File, Request

from app.src.object.utility.services.UtilityServices import UtilityServices

router = APIRouter()


@router.post('/uploadFile')
async def uploadImage(file: UploadFile = File(...)):
    return UtilityServices.getImgPath(file.filename, await file.read())


@router.post('/getStatementImage/{user_id}')
async def convertToImage(user_id: str, tokenHistory: Request):
    return UtilityServices.convertToImage(user_id, dict(await tokenHistory.json())["tokenHistory_id"],
                                          dict(await tokenHistory.json())["reward_id"])
