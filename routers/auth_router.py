from fastapi.responses import JSONResponse
from models.models import User,Login
from DB.db import user_col
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
import DB.db, bcrypt, jwt,time


authApp = FastAPI()

JWT_SECRET_KEY = "SECRETKEY"
JWT_ALGORITHM = "HS256"
@authApp.post("/create_user/")
def create_user(value: User):
    existing_user = user_col.find_one({"username": value.username})

    if existing_user:
        return JSONResponse(
            status_code=400,
            content={
                "status": "failed",
            },
        )

    new_value = value.dict()
    new_user = User(**new_value)
    new_user.hash_password()  # Hash the password
    result = user_col.insert_one(new_user.dict())
    inserted_id = result.inserted_id

    response_data = {
        "status": "success",
        "message": "User created successfully",
        "user_id": str(inserted_id),
        "username": value.username,
    }
    return JSONResponse(content=response_data)
def hash_password(raw_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(raw_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_token(user: User):
    ts = time.time()
    payload = {
        "user_id": str(DB.db.user_col.find_one({"username": user.username})["_id"]),
        "username": user.username,
        "timestamp": ts,
    }
    secret_key = JWT_SECRET_KEY
    token = jwt.encode(
        payload,
        secret_key,
        algorithm=JWT_ALGORITHM,
    )
    return token


@authApp.post('/login')
async def login(user: User):
    data = DB.db.user_col.find_one({"username": user.username}) # or {"username": user.username} depending on your schema
    if not data:
        # Return appropriate response if no matching user is found
        return JSONResponse(
            status_code=403,
            content={
                "status": "failed",
                "message": "No such user found",
            },
        )

    bcrypt_pass = str.encode(user.password)
    hashed = data["password"]
    if bcrypt.checkpw(bcrypt_pass, hashed):
        token = generate_token(user)
        return {"status": "success", "token": token}
    else:
        return JSONResponse(
            status_code=403,
            content={
                "status": "failed",
                "message": "Username or Password is wrong",
            },
        )
