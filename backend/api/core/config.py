from pydantic import BaseSettings, BaseModel
import os
class Settings(BaseSettings):
    #App Settings
    PROJECT_NAME: str = 'Sentra - API'
    APP_NAME: str = "Monitoring System - Backend"
    API_STR: str = "/api/v1"
    PROWLER_API_STR: str = "/api/prowler"

        
    # Database configuration
    # 데이터베이스 설정
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5433'))
    DB_NAME: str = os.getenv('DB_NAME', 'Sentra_DB')
    DB_USER: str = os.getenv('DB_USER', 'sentra_user')  
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'huni5504')  # Changed from PASSWORD to DB_PASSWORD
    
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    #JWT Settings
    #JWT 토큰 설정
    SECRET_KEY: str = '26mpViW3rldpRIrlqhPlzXSqbMscYMd8MCJHk6ipxus3YzAGXPS2PGQl2FqjDEyxH5OAHmFEAThkyGXJYetG1iY0byF32Slc6Tv3AHRtStHWec9UwK9HdSHQL2V0c5w94GzcAxlqg9udRcZ3tMwlLdMF63BZefU0TCYHBbmksI8vXIUXqc9LbxigEXpGG5GQjd009DxVGAEXU40yMJdCgX3mkJjDBtl4XM0Sa29HfWhdk8fL6I6Jdk5w5Krbd3Ie'
    TOKEN_LOCATION: set = {'cookies'}
    CSRF_PROTECT: bool = False
    COOKIE_SECURE: bool = False  # should be True in production
    COOKIE_SAMESITE: str = 'lax'  # should be 'lax' or 'strict' in production
    ACCESS_TOKEN_EXPIRES: int = 900  # 15 minutes = 900
    REFRESH_TOKEN_EXPIRES: int = 2592000  # 30 days = 2592000
    
    # ADMIN Settings
    # 사이트 관리자 계정 정보
    ADMIN_USERID: str = 'admin'
    ADMIN_USERNAME: str = 'kwanghun lee'
    ADMIN_EMAIL: str = 'gbhuni@gmail.com'
    ADMIN_PASSWORD: str = 'huni5504'
    ADMIN_COMPANY_NAME: str = 'Pusan National University'

settings = Settings()