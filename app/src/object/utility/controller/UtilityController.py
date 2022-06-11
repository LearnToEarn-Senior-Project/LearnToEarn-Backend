from fastapi import APIRouter, UploadFile, File

from app.src.object.utility.services.UtilityServices import UtilityServices

router = APIRouter()


@router.post('/uploadFile')
async def uploadImage(file: UploadFile = File(...)):
    return UtilityServices.getImgPath(file.filename, await file.read())
