import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import odic
from .config import settings
from dotenv import load_dotenv

load_dotenv()

version = os.getenv("version")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.cors_1,
        settings.cors_2
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(odic.router)

@app.get("/")
async def home():
    return {"health_check": "ok", "model_version": version}