import io
from bson import ObjectId
from firebase_admin import credentials, initialize_app, storage, get_app


class UtilityServices:
    @staticmethod
    def getImgPath(image_name, content):
        byte = io.BytesIO(content)
        cred = credentials.Certificate("../app/src/resources/learntoearn-cred.json")
        try:
            initialize_app(cred, {'storageBucket': 'learntoearn-350914.appspot.com'})
        except:
            get_app()
        bucket = storage.bucket()
        blob = bucket.blob(image_name + ObjectId().__str__())
        blob.upload_from_string(byte.read(), content_type='image/png')
        blob.make_public()
        return blob.public_url
