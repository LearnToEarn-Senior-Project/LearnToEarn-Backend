from fastapi import APIRouter
from app.src.server.database import DB
from app.src.object.evidence.services.EvidenceServices import EvidenceServices

router = APIRouter()

@router.get('/convertBillToImage')
async def convertToImage():
    EvidenceServices.convertToImage()

