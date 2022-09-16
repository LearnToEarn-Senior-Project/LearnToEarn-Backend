from app.src.server.database import DB
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

client_id = "726873603726-tq3t7s31jodv5qcu335dpn8beln6oise.apps.googleusercontent.com"
client_secret = "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"


def GoogleCredential(user_id):
    try:
        googleUser = list(DB.DATABASE['user'].find({"_id": user_id}).limit(1))[0]["google_object"]["user_token"]
        creds = Credentials.from_authorized_user_info({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": googleUser["refresh_token"]
        })

        creds.refresh(Request())
        DB.update(collection='user', id=user_id, data={
            "google_object.user_token.access_token": creds.__getstate__().get("token")
        })

        return build('classroom', 'v1', credentials=creds)
    except:
        return None


def RefreshToken(user_id):
    try:
        googleUser = list(DB.DATABASE['user'].find({"_id": user_id}).limit(1))[0]["google_object"]["user_token"]
        creds = Credentials.from_authorized_user_info({
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": googleUser["refresh_token"]
        })

        creds.refresh(Request())
        DB.update(collection='user', id=user_id, data={
            "google_object.user_token.access_token": creds.__getstate__().get("token")
        })
    except:
        return None
