# BUILT IN
import os
import sys
import traceback
import json


# EXTERNAL LIBRARIES
from typing import Union
from pydantic import BaseModel
#from pprint import pprint

# FASTAPI
from fastapi import FastAPI
from fastapi import Response
from fastapi import File
from fastapi import UploadFile
from fastapi import Form

# STARLETTE
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

# PROJECT LIB
#from dummy_ocr import resim_kontrol
from ocr_controller import OcrController
import crud_controller as cd


mock_products = {
            "totalBills": [
                {
                    "products": [
                        {
                            "Product Name": "ALTINORC TBIC 1 LLU",
                            "Amount": "9.95",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "INKILIG 1 L KEFIR",
                            "Amount": "7.95",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "AR 1 KG TARBYA",
                            "Amount": "34.90",
                            "IsLoss": "false"
                        }
                    ]
                },
                {
                    "products": [
                        {
                            "Product Name": "KENTIRASKOPU30",
                            "Amount": "15.90",
                            "IsLoss": "true"
                        },
                        {
                            "Product Name": "KG SUCUK 250G",
                            "Amount": "51.95",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "BG HOT DORITOS",
                            "Amount": "15.95",
                            "IsLoss": "true"
                        },
                        {
                            "Product Name": "MİGROS 2L AYRAN",
                            "Amount": "10.50",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "ÜLKER ÇİKOLATA",
                            "Amount": "7.75",
                            "IsLoss": "true"
                        }
                    ]
                },
                {
                    "products": [
                        {
                            "Product Name": "KLAMA KAB1 3 LU CO",
                            "Amount": "9.95",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "FST 1 25 L",
                            "Amount": "42.95",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "SACTI SALAM 75",
                            "Amount": "23.50",
                            "IsLoss": "true"
                        },
                        {
                            "Product Name": "TURKCELL TL YÜKLEME",
                            "Amount": "20.00",
                            "IsLoss": "false"
                        }
                    ]
                },
                {
                    "products": [
                        {
                            "Product Name": "UNO EKMEK",
                            "Amount": "4.50",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "COKE 1L",
                            "Amount": "5.95",
                            "IsLoss": "true"
                        },
                        {
                            "Product Name": "NESTLE 250G KAHVE",
                            "Amount": "28.90",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "PRİL 1L DETERJAN",
                            "Amount": "18.50",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "LAV 6LI BARDAK",
                            "Amount": "24.75",
                            "IsLoss": "false"
                        }
                    ]
                },
                {
                    "products": [
                        {
                            "Product Name": "YUDUM 1L YAĞ",
                            "Amount": "26.95",
                            "IsLoss": "true"
                        },
                        {
                            "Product Name": "DİMES 1L MEYVE SUYU",
                            "Amount": "12.75",
                            "IsLoss": "false"
                        },
                        {
                            "Product Name": "PIRLANTA 1KG PİRİNÇ",
                            "Amount": "18.95",
                            "IsLoss": "false"
                        }
                    ]
                }
            ]
        }
test_gemini = {'products': [{'Amount': 3.12, 'Product Name': 'VAHM - NOVA MOROA'},
              {'Amount': 3.98, 'Product Name': 'LO DE ME OCES -'},
              {'Amount': 3.14, 'Product Name': 'KUMBERLEY - KALEN - BXE'},
              {'Amount': 3.1, 'Product Name': 'HAYRETTIN TASKAVA - KANI'},
              {'Amount': 3.37, 'Product Name': 'BENIMLE MAYBOLUN - KANI'},
              {'Amount': 4.21, 'Product Name': 'YOGUNLUK VE AGRILAR - KANI'},
              {'Amount': 4.07, 'Product Name': 'BOS SNACK -'},
              {'Amount': 4.24, 'Product Name': 'EL ACARHI - CEYLAN EREM'},
              {'Amount': 4.12, 'Product Name': 'ANHARA JOA BIRI VAR - CAN'},
              {'Amount': 3.48, 'Product Name': 'CIKTIM BI YOLA - NOVA'},
              {'Amount': 3.05, 'Product Name': 'GUNCOR -'},
              {'Amount': 3.52, 'Product Name': 'KAZAZ -'},
              {'Amount': 3.1, 'Product Name': 'INCHIZE CAURA - CAN'}]}

# CONSTANTS
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.svg', '.webp', '.ico']


# FastAPI instance
app = FastAPI(redoc_url=None)


# API BODY MODELS
# Used for get_recommendation endpoint
class User(BaseModel):
    user_uuid: str
    shop_name: str

class Bill(BaseModel):
    user_uid: str
    user_mail: str
    products: str # Response from gemini will sent by the user.

class UserMail(BaseModel):
    user_mail: str

class Deneme(BaseModel):
    uid: str
    img: UploadFile = File(...)



# DUMMY MAIN ROOT
@app.get("/")
async def main_root(
        response: Response):
    response.status_code = HTTP_405_METHOD_NOT_ALLOWED


# UPLOAD IMAGE ENDPOINT
@app.post("/upload_picture")
async def upload_picture(
        response: Response,
        file: UploadFile = File(...),
        user_uuid: str = Form(...),
        shop_name: str = Form(...)):

        #ocr_controller = OcrController()
        #ocr_controller.save_image(file)
        """
        NORMALLY, HANDLING I/O PROCESSES ON API LAYER IS 
        A DANGEROUS APPROACH TO TAKE. BUT TO BE FAST, WE
        IMPLEMENTED IN THIS WAY. WE MAY CHANGE THIS LATER.
        """
        try:
            print("-----> API Layer: image saving.")
            directory = "temp_pictures"
            file_path = os.path.join(directory, file.filename)
            with open(file_path, "wb") as img:
                img.write(await file.read())
            print("-----> API Layer: image saved.")
            #print(user_uuid,shop_name)
            return 
        
        except Exception:
            print("-----> OcrController: an exception occured at save_image !")
            print(traceback.format_exc())
            return 11
        


# GET USER BILLS FROM DATABASE.
@app.post("/get_user_bills")
async def get_bills(
        body: User,
        response: Response
):
    if len(body.user_uuid) != 0:
        response.status_code = HTTP_200_OK

    else:
        response.status_code = HTTP_405_METHOD_NOT_ALLOWED


# GET RECOMMENDATIONS
@app.post("/call_rec_method")
async def get_recommendation():
    pass


# UPLOAD BILL ENDPOINT FOR MOBILE
# APPLICATION SIDE
@app.post("/upload_bill_mobile")
async def upload_bill_json(products: Bill,
                           response: Response):
    print("-----> upload_bill_mobile endpoint test:")
    print(products.user_uid)
    print(products.user_mail)
    print(products.products)

    products_dict = json.loads(products.products)


    user_exists = cd.user_exist(products.user_mail)
    if user_exists is False:
        cd.create_user(products.user_mail,
                       products.user_uid)
        cd.create_bill(products.user_mail,
                       products_dict)
        
    
    else:
        cd.create_bill(products.user_mail,
                       products_dict)

    
    
    return {"sualp":32}


# MOBILE HISTORY ENDPOINT FOR GATHERING PREVIOUS
# RECEIPT RECORDS
@app.post("/get_bill_history")
async def get_bills_mobile(response: Response,
                           user_credential: UserMail) -> dict | None | int:
    
    user_bills_products = cd.get_all_bills_with_products(user_credential.user_mail)
    return user_bills_products