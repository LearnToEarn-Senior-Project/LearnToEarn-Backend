from fastapi import APIRouter

from app.src.object.classroom.services.GoogleClassroomServices import GoogleClassroomServices

router = APIRouter()


@router.get('/getGoogleClassrooms/{id}/page={page}')
async def getAllGoogleClassrooms(id: str, page: int):
    return GoogleClassroomServices.getAllPagination(id, page)


@router.get('/getClassroomWithAssignment/{id}/{course_id}')
async def getGoogleClassroomsByIdWithAssignment(id: str, course_id: str):
    return GoogleClassroomServices.getByIdWithAssignment(id, course_id)


@router.get('/getClassroom/{course_id}')
async def getGoogleClassroomsById(course_id: str):
    return GoogleClassroomServices.getById(course_id)
