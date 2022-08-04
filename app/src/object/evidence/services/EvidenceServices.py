import base64
import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from app.src.server.database import DB
from sklearn.externals._pilutil import imsave


class EvidenceServices:
    @staticmethod
    def convertToImage(user_id, transaction_id, reward_id):
        userName = list(
            DB.DATABASE["user"].find({"_id": user_id}, {"firstname": True, "lastname": True, "_id": False}).limit(1))[0]
        fullName = userName["firstname"] + " " + userName["lastname"]
        transactionInformation = list(DB.DATABASE["tokenHistory"].find({"_id": transaction_id}).limit(1))[0]
        if transactionInformation["checked"] is True:
            img = Image.open("../app/src/resources/LTE_BillBackgroundApproved.jpg")
        else:
            img = Image.open("../app/src/resources/LTE_BillBackground.jpg")
        reward = list(DB.DATABASE["reward"].find({"_id": reward_id}).limit(1))[0]
        I1 = ImageDraw.Draw(img)
        font = "../app/src/resources/Helvetica.ttf"
        # Add Text to an image
        font_Header = ImageFont.truetype(font, 20)
        font_Name = ImageFont.truetype(font, 40)
        font_detail = ImageFont.truetype(font, 20)
        font_thanks1 = ImageFont.truetype(font, 22)
        font_thanks2 = ImageFont.truetype(font, 15)

        # Add Text to an image
        I1.text((525, 20), "Bill ID: " + transaction_id, font=font_thanks2, fill=(0, 0, 0))
        I1.text((525, 45), "Date: " + transactionInformation["date"], font=font_thanks2, fill=(0, 0, 0))

        I1.text((55, 130), "Reward to", font=font_Header, fill=(0, 0, 0))
        I1.text((100, 165), fullName, font=font_Name, fill=(0, 0, 0))
        I1.text((100, 215), "Student ID: " + user_id, font=font_detail, fill=(0, 0, 0))

        I1.text((55, 295), "Item", font=font_Header, fill=(0, 0, 0))
        I1.text((55, 339), reward["name"], font=font_detail, fill=(0, 0, 0))
        I1.text((625, 295), "Price", font=font_Header, fill=(0, 0, 0))
        I1.text((625, 339), str(reward["price"]), font=font_detail, fill=(0, 0, 0))
        I1.text((442, 402), "Total price", font=font_Header, fill=(0, 0, 0))
        I1.text((625, 402), str(reward["price"]), font=font_detail, fill=(0, 0, 0))
        I1.text((235, 483), "Thanks to the intended learning", font=font_thanks1, fill=(0, 0, 0))
        I1.text((287, 514), "This is a reward for your effort", font=font_thanks2, fill=(0, 0, 0))
        buf = io.BytesIO()
        imsave(buf, img, format='PNG')
        buf.seek(0)
        return str(base64.b64encode(buf.getvalue()))[2::][:-1]
