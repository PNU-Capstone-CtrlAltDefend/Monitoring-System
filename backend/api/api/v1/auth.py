from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from fastapi_jwt_auth import AuthJWT

from fastapi import status
from core.security import verify_password  # 비밀번호 비교 함수
from fastapi_jwt_auth.exceptions import AuthJWTException

from core.security import get_password_hash

from model.database import get_db
from model.security_manager import schemas as security_manager_schemas  
from model.security_manager import crud as security_manager_crud

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/signup')
async def sign_up(form_data: security_manager_schemas.UserCreate , Authorize: Annotated[AuthJWT, Depends()], db: Annotated[Session, Depends(get_db)]):
    """
    회원가입 엔드포인트
    """
    user = security_manager_crud.get_security_manager_by_id(db, form_data.manager_id)

    existing = security_manager_crud.get_security_manager_by_id(db, form_data.manager_id)
    if existing:
        raise HTTPException(status_code=400, detail='이미 존재하는 ID입니다.')

    new_user = security_manager_crud.create_security_manager(db, form_data)
    
    if not new_user:
        raise HTTPException(status_code=400, detail='회원가입에 실패했습니다.')

    return {'msg': 'Signed up successfully'}

@router.post('/signin')
async def sign_in(
    Authorize: Annotated[AuthJWT, Depends()],
    db: Annotated[Session, Depends(get_db)],
    form_data: OAuth2PasswordRequestForm = Depends()  # 마지막에 둠
):
    """
    로그인 엔드포인트
    """
    user = security_manager_crud.get_security_manager_by_id(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='잘못된 ID 또는 비밀번호입니다.')

    # JWT 토큰 생성
    access_token = Authorize.create_access_token(subject=user.manager_id)
    refresh_token = Authorize.create_refresh_token(subject=user.manager_id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }