from fastapi import FastAPI, HTTPException, Request
import jwt
from routers.user_router import userApp
from routers.auth_router import authApp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/user", userApp)
app.mount("/auth", authApp)

origins = [
   "http://192.168.211.:8000",
   "http://localhost",
   "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

