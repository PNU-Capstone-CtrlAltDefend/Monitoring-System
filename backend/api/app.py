from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader

from model.init_database import init_database
from model.database import engine, SessionLocal
from core.config import settings

# API 모듈 
from api.v1 import auth 
from api.v1 import organizations
from api.v1 import topology

from api.v1.router import network_monitor
from api.v1.router import log_collector

print(
"""   
======================================        
 _____               _                
/  ___|             | |               
\ `--.   ___  _ __  | |_  _ __   __ _ 
 `--. \ / _ \| '_ \ | __|| '__| / _` |
/\__/ /|  __/| | | || |_ | |   | (_| |
\____/  \___||_| |_| \__||_|    \__,_|
 S  E  N  T  R  A  •  S E C U R I T Y
======================================                                 
""")
try:
    init_database(engine, SessionLocal())
except Exception as e:
    print(f"Database initialization failed: {e}")
    print("The API will start but database operations may fail until connection is established")

auth_header = APIKeyHeader(name="Authorization", auto_error=False)
app = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f"{settings.API_STR}/openapi.json",
              dependencies=[Depends(auth_header)],
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
app.include_router(organizations.router, prefix=settings.API_STR, tags=['Organizations'])
app.include_router(topology.router, prefix=settings.API_STR, tags=['Topology'])

app.include_router(network_monitor.router, prefix=settings.API_STR, tags=['Network Monitor'])
app.include_router(log_collector.router, prefix=settings.API_STR, tags=['Log Collector'])