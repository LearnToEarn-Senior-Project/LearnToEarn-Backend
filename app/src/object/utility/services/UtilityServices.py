import io
from bson import ObjectId
from firebase_admin import credentials, initialize_app, storage, get_app


class UtilityServices:
    @staticmethod
    def getImgPath(image_name, content):
        try:
            byte = io.BytesIO(content)
            cred = credentials.Certificate("../app/src/resources/LearnToEarn-Firebase-Credential.json")
            try:
                initialize_app(cred, {'storageBucket': 'learntoearn-350914.appspot.com'})
            except:
                get_app()
            bucket = storage.bucket()
            if image_name.split(".")[-1] in ["jpg", "jpeg", "png", "webp"]:
                blob = bucket.blob(image_name + ObjectId().__str__())
                blob.upload_from_string(byte.read(), content_type='image/png')
                blob.make_public()
                return blob.public_url
            else:
                return "File type must be image only"
        except:
            return "The input is not complete"
