import datetime
import bcrypt
from fastapi import FastAPI, HTTPException, Request,APIRouter
import jwt
from DB.db import user_col
from models.models import Qr,User
from fastapi.responses import JSONResponse
from bson import ObjectId  # Import ObjectId
import datetime


userApp = FastAPI()
userRouter = APIRouter(tags=['Users'])

JWT_SECRET_KEY = "SECRETKEY"
JWT_ALGORITHM = "HS256"

@userApp.middleware("http")
async def user_middleware(request: Request, call_next):
    headers = request.headers
    if "Authorization" in headers:
        token = request.headers["Authorization"]
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            request.state.username = data["username"]
            request.state.userID = data["user_id"]
        except:
            return JSONResponse(
                status_code=403,
                content={
                    "status": "failed",
                    "message": "Authentication Failed",
                },
            )
    else:
        return JSONResponse(
            status_code=403,
            content={
                "status": "failed",
                "message": "Authentication Failed",
            },
        )
    response = await call_next(request)
    return response

@userApp.post("/addQr")
async def add_course(value: Qr, request: Request):
    try:
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
        
        # Create a new QR data with enterTime and empty outTime
        qr_data = {
            "location": value.location,
            "enterTime": formatted_datetime,
            "outTime": ""
        }

        # Update user's data field
        user_col.update_one(
            {"_id": ObjectId(request.state.userID)}, {"$push": {"data": qr_data}}
        )
        return {"message": "Qr Value Added Successfully"}

    except:
        return JSONResponse(
            status_code=403,
            content={
                "status": "failed",
                "message": "Couldn't add the Qr Value!",
            },
        )

@userApp.put("/update_end_time")
async def update_end_time(value: Qr, request: Request):
    try:
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
        
        # Find the user's QR data with the given location and empty outTime and update it
        response = user_col.update_one(
            {
                "_id": ObjectId(request.state.userID),
                "data": {
                    "$elemMatch": {
                        "location": value.location,
                        "outTime": ""
                    }
                }
            },
            {
                "$set": {"data.$.outTime": formatted_datetime}
            }
        )

        if response.modified_count == 0:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "failed",
                    "message": "Couldn't find the location with empty outTime for this user!",
                },
            )

        return {"message": "Qr outTime Updated Successfully"}

    except:
        return JSONResponse(
            status_code=403,
            content={
                "status": "failed",
                "message": "Couldn't update the Qr outTime!",
            },
        )
