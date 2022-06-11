from fastapi import APIRouter

from app.src.object.criteria.services.CriteriaServices import CriteriaServices

router = APIRouter()


@router.get('/criteria')
async def getAllCriteria():
    return CriteriaServices.getAll()
