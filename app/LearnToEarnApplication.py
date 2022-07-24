import uvicorn
import multiprocessing as mp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.src.object.token.controller import TokenController
from app.src.object.reward.controller import RewardController
from app.src.object.utility.controller import UtilityController
from app.src.object.criteria.controller import CriteriaController
from app.src.object.user.CMUUser.controller import CMUUserController
from app.src.object.assignment.controller import AssignmentController
from app.src.object.user.GoogleUser.controller import GoogleUserController
from app.src.object.classroom.controller import GoogleClassroomController
from app.src.object.tokenHistory.controller import TokenHistoryController

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000/",
    "http://127.0.0.1:3000/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(TokenController.router)
app.include_router(RewardController.router)
app.include_router(UtilityController.router)
app.include_router(CriteriaController.router)
app.include_router(CMUUserController.router)
app.include_router(GoogleUserController.router)
app.include_router(GoogleClassroomController.router)
app.include_router(AssignmentController.router)
app.include_router(TokenHistoryController.router)

if __name__ == "__main__":
    uvicorn.run("LearnToEarnApplication:app", reload=True, port=5000, workers=mp.cpu_count())
