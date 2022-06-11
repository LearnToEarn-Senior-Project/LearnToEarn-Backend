from fastapi import APIRouter

from app.src.object.classroom.GoogleClassroom.Services.GoogleClassroomServices import GoogleClassroomServices

router = APIRouter()


@router.get('/getGoogleClassrooms/{id}/page={page}')
async def getAllGoogleClassrooms(id: str, page: int):
    return GoogleClassroomServices.getAllPagination(id, page, 4)
