from fastapi import APIRouter, Request

from app.src.object.criteria.services.CriteriaServices import CriteriaServices

router = APIRouter()


@router.post('/setCriteria')
async def setCriteria(criteria: Request):
    return CriteriaServices.add(dict(await criteria.json())['id'],
                                dict(await criteria.json())['first'],
                                dict(await criteria.json())['second'],
                                dict(await criteria.json())['third'])


@router.get('/getCriteria/{course_id}')
async def getCriteriaInCourse(course_id: str):
    return CriteriaServices.get(course_id)
