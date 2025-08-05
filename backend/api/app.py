from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from model.init_database import init_database
from model.database import engine, SessionLocal
from core.config import settings
from api.v1 import auth 
try:
    init_database(engine, SessionLocal())
except Exception as e:
    print(f"Database initialization failed: {e}")
    print("The API will start but database operations may fail until connection is established")

app = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f"{settings.API_STR}/openapi.json",
              debug=True)

origins = [
    "http://localhost:3001",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 또는 ["*"] 로 모든 도메인 허용 가능 (주의)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_STR, tags=['auth'])