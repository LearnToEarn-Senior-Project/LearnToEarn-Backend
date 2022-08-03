from fastapi import APIRouter, Request
from app.src.object.evidence.services.EvidenceServices import EvidenceServices

router = APIRouter()


@router.post('/getBillImage/{user_id}')
async def convertToImage(user_id: str, transaction: Request):
    return EvidenceServices.convertToImage(user_id, dict(await transaction.json())["transaction_id"],
                                           dict(await transaction.json())["reward_id"])
