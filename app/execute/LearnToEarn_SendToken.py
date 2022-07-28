import pytz
import uvicorn
import multiprocessing as mp

from fastapi import FastAPI
from datetime import datetime
from fastapi_utils.tasks import repeat_every
from app.src.object.token.services.TokenServices import TokenServices

sendToken = FastAPI()


@sendToken.on_event("startup")
@repeat_every(wait_first=True, seconds=1)
async def sendStudentToken():
    # print(counts.count1())
    TokenServices.sendToken()
    if datetime.now(pytz.timezone('Asia/Bangkok')).strftime("%H:%M:%S").__str__() == "00:00:00":
        return await TokenServices.sendToken()


class counts:
    count = 0

    @staticmethod
    def count1():
        counts.count += 1
        return counts.count


if __name__ == "__main__":
    uvicorn.run("LearnToEarn_SendToken:sendToken", reload=True, port=5100, workers=mp.cpu_count())
