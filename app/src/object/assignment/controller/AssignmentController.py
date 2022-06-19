from fastapi import APIRouter

from app.src.object.assignment.services.AssignmentServices import AssignmentServices

router = APIRouter()


@router.get('/getAssignments/{user_id}/{course_id}')
async def getAllAssignments(user_id: str, course_id: str):
    return AssignmentServices.getAll(user_id, course_id)
