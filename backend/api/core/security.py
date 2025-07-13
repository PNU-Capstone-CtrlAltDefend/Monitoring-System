from passlib.context import CryptContext

# 비밀번호 해시 생성을 위한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 해시 생성
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 🔒 해시 검증 (로그인 시 사용)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)