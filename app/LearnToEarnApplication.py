import uvicorn
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.src.entity.token.token import Token
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
@app.get("/rewards/page={page}")
async def getAllRewardsWithPagination(page: int):
    return Reward.getRewardsPagination(page, 10)


@app.get('/reward/{reward_id}')
async def getRewardByID(reward_id: str):
    return Reward.getRewardByID(reward_id)


@app.post('/addReward')
async def adminAddReward(reward: Request):
    try:
        image = dict(await reward.json())['image']
    except:
        image = None
    reward = Reward(dict(await reward.json())["name"],
                    dict(await reward.json())["detail"],
                    dict(await reward.json())['amount'],
                    dict(await reward.json())['price'], image)

    return reward.addReward()


@app.delete('/deleteReward/{reward_id}')
async def adminDeleteReward(reward_id: str):
    Reward.deleteReward(reward_id)
    return "Delete reward successfully!!"


@app.post('/uploadFile')
async def uploadImage(file: UploadFile = File(...)):
    return Reward.getImgPath(file.filename, await file.read())


@app.patch('/updateReward/{reward_id}')
async def adminUpdateReward(reward_id: str, reward: Request):
    try:
        image = dict(await reward.json())['image']
    except:
        image = list(DB.DATABASE['reward'].find({"_id": reward_id}).limit(1))[0]["image"]
    return Reward.updateReward(reward_id, dict(await reward.json())["name"], dict(await reward.json())["detail"],
                               dict(await reward.json())["amount"], dict(await reward.json())["price"],
                               image)


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
    cmuUser = User(dict(await user.json())['id'],
                   dict(await user.json())['firstname'],
                   dict(await user.json())['lastname'],
                   dict(await user.json())['email'],
                   None,
                   dict(await user.json())['role'])
    return cmuUser.addUser()


@app.get('/getRole/{id}')
async def getUserRole(id: str):
    return list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0].get("role")


@app.get('/swapRole/{id}')
async def swapRole(id: str):
    data = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]
    arr = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0].get("role")
    tmp = arr[0]
    arr[0] = arr[1]
    arr[1] = tmp
    DB.update(collection='user', id=id, data={
        '_id': id,
        'firstname': data.get("firstname"),
        'lastname': data.get("lastname"),
        'email': data.get("email"),
        'google_object': data.get("google_object"),
        'role': arr,
        'current_token': data.get("current_token")
    })
    return arr


# =========================== CMU session =============================
# =========================== Criteria session =============================
@app.get('/criteria')
async def getAllCriteria():
    return Criteria.getAllCriteria()


# =========================== Criteria session =============================
# =========================== Token session =============================

@app.post('/addToken')
async def addToken(add: Request):
    token = Token(dict(await add.json())['amount'])
    return token.addToken()


@app.get('/getAllToken')
async def getToken():
    print(DB.DATABASE['token'].find({"_id": "1"}).limit(1)[0]["amount"])
    return DB.DATABASE['token'].find({"_id": "1"}).limit(1)[0]["amount"]


@app.get('/studentToken/{id}')
async def getStudentToken(id: str):
    return Token.getStudentToken(id)


# =========================== Token session =============================

if __name__ == "__main__":
    uvicorn.run("LearnToEarnApplication:app", reload=True, port=5000, workers=mp.cpu_count())
