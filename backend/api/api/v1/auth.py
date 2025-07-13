from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from fastapi_jwt_auth import AuthJWT

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
    user = security_manager_crud.get_security_manager_by_id(db, form_data.manager_id)

    existing = security_manager_crud.get_security_manager_by_id(db, form_data.manager_id)
    if existing:
        raise HTTPException(status_code=400, detail='이미 존재하는 ID입니다.')

    new_user = security_manager_crud.create_security_manager(db, form_data)
    
    if not new_user:
        raise HTTPException(status_code=400, detail='회원가입에 실패했습니다.')

    return {'msg': 'Signed up successfully'}
