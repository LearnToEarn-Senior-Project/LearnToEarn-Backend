import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.database import DB
from app.src.entity.classroom.classroom import Classroom
from app.src.entity.reward.reward import Reward
from app.src.entity.criteria.criteria import Criteria
from app.src.entity.user.googleUser import GoogleUser
from app.src.entity.user.user import User
import multiprocessing as mp

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DB()


# ========================= Reward session ============================
@app.get("/rewards")
async def getAllRewards():
    return Reward.getRewardsPagination(2, 8)


@app.get('/reward/{reward_id}')
async def getRewardByID(reward_id: str):
    return Reward.getRewardByID(reward_id)


@app.post('/addReward')
async def adminAddReward(reward: Request):
    reward = Reward(dict(await reward.json())["name"],
                    dict(await reward.json())["detail"],
                    dict(await reward.json())['amount'],
                    dict(await reward.json())['price'],
                    dict(await reward.json())['image'])
    return reward.addReward()


@app.delete('/deleteReward/{reward_id}')
async def adminDeleteReward(reward_id: str):
    Reward.deleteReward(reward_id)
    return "Delete reward successfully!!"


@app.patch('/updateReward/{reward_id}')
async def adminUpdateReward(reward_id: str, reward: Request):
    return Reward.updateReward(reward_id, dict(await reward.json())["name"], dict(await reward.json())["detail"],
                               dict(await reward.json())["amount"], dict(await reward.json())["price"],
                               dict(await reward.json())["image"])


# ========================= End Reward session ============================
# ========================= Google session ============================

@app.post('/google_login')
async def getGoogleToken(googleUser: Request):
    return GoogleUser.bindGoogleAccount(dict(await googleUser.json())['id'], dict(await googleUser.json())['auth_code'])


@app.post('/google_logout')
async def googleLogout(googleUser: Request):
    return GoogleUser.unbindGoogleAccount(dict(await googleUser.json())['id'])


@app.get('/googleGetData/{id}')
async def googleGetData(id: str):
    return GoogleUser.getUserGoogleData(id)


# ========================= Google session ============================
# =========================== CMU session =============================
@app.get('/getGoogleClassrooms/{id}')
async def getAllGoogleClassrooms(id: str):
    return Classroom.getAllGoogleClassrooms(id)


@app.post('/login/{code}')
async def CMUOAuthLogin(code: str):
    return User.getAccessToken(code)


@app.get('/credentials/{token}')
async def CMUOAuthGetUserData(token: str):
    return User.getCredentials(token)


@app.get('/getUser/{id}')
async def CMUOAuthGetUserByID(id: str):
    return User.getUser(id)


@app.post('/addUser')
async def CMUOAuthSaveUser(user: Request):
    cmuUser = User(dict(await user.json())["name"],
                   dict(await user.json())['firstname'],
                   dict(await user.json())['lastname'],
                   dict(await user.json())['email'],
                   None,
                   dict(await user.json())['role'])
    return cmuUser.addUser()


# =========================== CMU session =============================
# =========================== Criteria session =============================

@app.get('/criteria')
async def getAllCriteria():
    return Criteria.getAllCriteria()


# =========================== Criteria session =============================

if __name__ == "__main__":
    uvicorn.run("LearnToEarnApplication:app", reload=True, port=5000, workers=mp.cpu_count())
