from fastapi import APIRouter, Request

from app.src.object.tokenHistory.services.TokenHistoryServices import TokenHistoryServices

router = APIRouter()


@router.get('/getAllTokenHistory/{id}/page={page}/bool={checked}')
async def getAllTokenHistoryForStudent(id: str, page: int, checked: bool):
    return TokenHistoryServices.getAllPagination(id, page, checked)


@router.get('/getAllTokenHistory/page={page}')
async def getAllTokenHistoryForAdmin(page: int):
    return TokenHistoryServices.getAllForApproval(page)


@router.patch('/approveBill/{transaction_id}')
async def approveBill(transaction_id: str):
    return TokenHistoryServices.approve(transaction_id)


@router.post('/addHistory/{student_id}')
async def addHistory(student_id: str, reward: Request):
    return TokenHistoryServices.add(dict(await reward.json())["amount"], student_id,
                                    dict(await reward.json())["_id"])
