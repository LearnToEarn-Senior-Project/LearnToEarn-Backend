import io
import base64
import os

import qrcode
from PIL import Image, ImageOps, ImageDraw, ImageFont
from bson import ObjectId
from app.src.server.database import DB
from sklearn.externals._pilutil import imsave
from firebase_admin import credentials, initialize_app, storage, get_app


class UtilityServices:
    @staticmethod
    def getImgPath(image_name, content):
        try:
            byte = io.BytesIO(content)
            cred = credentials.Certificate(
                os.path.join(os.path.dirname(__file__), "LearnToEarn-Firebase-Credential.json"))
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

    @staticmethod
    def convertToImage(user_id, tokenHistory_id, reward_id):
        try:
            try:
                list(
                    DB.DATABASE["reward"].find({"_id": reward_id},
                                               {"amountOfCoin": True, "price": True, "_id": False}).limit(
                        1))[0]
            except:
                return "Reward not found"
            try:
                list(DB.DATABASE['user'].find({"_id": user_id}, {"current_token": True, "_id": False}))[0][
                    "current_token"]
            except:
                return "Student not found"
            try:
                list(
                    DB.DATABASE["tokenHistory"].find({"_id": tokenHistory_id}).limit(
                        1))[0]
            except:
                return "Token History not found"
            userName = list(
                DB.DATABASE["user"].find({"_id": user_id}, {"firstname": True, "lastname": True, "_id": False}).limit(
                    1))[0]
            fullName = userName["firstname"] + " " + userName["lastname"]
            tokenHistoryInformation = list(DB.DATABASE["tokenHistory"].find({"_id": tokenHistory_id}).limit(1))[0]
            if tokenHistoryInformation["checked"] is True:
                img = Image.open("../app/src/resources/LTE_BillBackgroundApproved.jpg")
            else:
                img = Image.open("../app/src/resources/LTE_BillBackground.jpg")
            reward = list(DB.DATABASE["reward"].find({"_id": reward_id}).limit(1))[0]
            I1 = ImageDraw.Draw(img)
            buf = io.BytesIO()

            font = "../app/src/resources/Helvetica.ttf"
            # Add Text to an image
            font_Header = ImageFont.truetype(font, 20)
            font_Name = ImageFont.truetype(font, 40)
            font_detail = ImageFont.truetype(font, 20)
            font_thanks1 = ImageFont.truetype(font, 22)
            font_thanks2 = ImageFont.truetype(font, 15)
            qrCode = qrcode.QRCode(
                version=1,
                box_size=4,
                border=1)
            qrCode.add_data(tokenHistory_id)
            qrCode.make(fit=True)
            qrImg = qrCode.make_image()

            # Add Text to an image
            I1.text((490, 20), "Token History ID: " + tokenHistory_id, font=font_thanks2, fill=(0, 0, 0))
            I1.text((490, 45), "Date: " + tokenHistoryInformation["date"], font=font_thanks2, fill=(0, 0, 0))

            I1.text((55, 130), "Reward to", font=font_Header, fill=(0, 0, 0))
            I1.text((100, 165), fullName, font=font_Name, fill=(0, 0, 0))
            I1.text((100, 215), "Student ID: " + user_id, font=font_detail, fill=(0, 0, 0))

            I1.text((55, 295), "Item", font=font_Header, fill=(0, 0, 0))
            I1.text((55, 339), reward["name"], font=font_detail, fill=(0, 0, 0))
            I1.text((625, 295), "Price", font=font_Header, fill=(0, 0, 0))
            I1.text((625, 339), str(reward["price"]), font=font_detail, fill=(0, 0, 0))
            I1.text((442, 402), "Total price", font=font_Header, fill=(0, 0, 0))
            I1.text((625, 402), str(reward["price"]), font=font_detail, fill=(0, 0, 0))
            I1.text((250, 475), "Thanks to the intended learning", font=font_thanks1, fill=(0, 0, 0))
            I1.text((295, 505), "This is a reward for your effort", font=font_thanks2, fill=(0, 0, 0))
            if tokenHistoryInformation["checked"] is False:
                I1.text((40, 500), "For admin, scan here", font=font_thanks2, fill=(0, 0, 0))
                I1.text((30, 520), "to approve this statement", font=font_thanks2, fill=(0, 0, 0))
                I1.bitmap((55, 390), ImageOps.invert(qrImg), fill=(0, 0, 0))
            # I1.bitmap((55, 490), code128.image(tokenHistory_id).resize((250, 50)), fill=(0, 0, 0))
            imsave(buf, img, format='PNG')

            buf.seek(0)
            return str(base64.b64encode(buf.getvalue()))[2::][:-1]
        except:
            return []
