from fastapi import APIRouter

from app.src.object.classroom.classroom.GoogleClassroom.Services.GoogleClassroomServices import GoogleClassroomServices

router = APIRouter()


@router.get('/getGoogleClassrooms/{id}/page={page}')
async def getAllGoogleClassrooms(id: str, page: int):
    return GoogleClassroomServices.getAllPagination(id, page)


@router.get('/getClassroom/{id}/{course_id}')
async def getAllGoogleClassrooms(id: str, course_id: str):
    return GoogleClassroomServices.getById(id, course_id)
