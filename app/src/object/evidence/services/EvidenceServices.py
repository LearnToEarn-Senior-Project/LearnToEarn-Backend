from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class EvidenceServices:
    @staticmethod
    def convertToImage():
        img = Image.open("../app/src/resources/LTE_BillBackground.jpg")
        I1 = ImageDraw.Draw(img)

        # Add Text to an image
        font_Header = ImageFont.truetype('Helvetica', 20)
        font_Name = ImageFont.truetype('Helvetica', 40)
        font_detail = ImageFont.truetype('Helvetica', 20)
        font_thanks1 = ImageFont.truetype('Helvetica', 22)
        font_thanks2 = ImageFont.truetype('Helvetica', 15)

        # Add Text to an image
        I1.text((525, 20), "Bill ID: 629c332d0b6f0d01bf6f91a8", font=font_thanks2, fill=(0, 0, 0))
        I1.text((525, 45), "Date: 14 August 2022", font=font_thanks2, fill=(0, 0, 0))

        I1.text((55, 130), "Reward to", font=font_Header, fill=(0, 0, 0))
        I1.text((100, 165), "Decha Laowraddecha", font=font_Name, fill=(0, 0, 0))
        I1.text((110, 215), "Remain token: 8 Tokens", font=font_detail, fill=(0, 0, 0))

        I1.text((55, 295), "Item", font=font_Header, fill=(0, 0, 0))
        I1.text((55, 339), "CAMT Pen", font=font_detail, fill=(0, 0, 0))
        I1.text((395, 295), "Remain amount", font=font_Header, fill=(0, 0, 0))
        I1.text((420, 339), "5 Left", font=font_detail, fill=(0, 0, 0))
        I1.text((600, 295), "Price", font=font_Header, fill=(0, 0, 0))
        I1.text((625, 339), "2 Tokens", font=font_detail, fill=(0, 0, 0))
        I1.text((442, 402), "Total price", font=font_Header, fill=(0, 0, 0))
        I1.text((625, 402), "2 Tokens", font=font_detail, fill=(0, 0, 0))

        I1.text((235, 483), "Thanks to the intended learning", font=font_thanks1, fill=(0, 0, 0))
        I1.text((287, 514), "This is a reward for your effort", font=font_thanks2, fill=(0, 0, 0))
        # Display edited image
        img.show()

        # Save the edited image
        img.save("D:\\Course\\Fourth year\\First term\\Senior Project\\LearnToEarn\\LearnToEarn-Backend\\app\\src\\resources\\test1.png")


