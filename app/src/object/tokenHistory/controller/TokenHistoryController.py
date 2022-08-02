from fastapi import APIRouter

from app.src.object.tokenHistory.services.TokenHistoryServices import TokenHistoryServices

router = APIRouter()


@router.get('/getAllTokenHistory/{id}/page={page}')
async def getAllTokenHistory(id: str, page: int):
    return TokenHistoryServices.getAllPagination(id, page)
