import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import odic
from dotenv import load_dotenv

load_dotenv()

version = os.getenv("version")

app = FastAPI()

cors1 = os.getenv("cors_1")
cors2 = os.getenv("cors_2")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        cors1,
        cors2
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(odic.router)

@app.get("/")
async def home():
    return {"health_check": "ok", "model_version": version}