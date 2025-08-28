
from fastapi import APIRouter, Depends, HTTPException, status
from model.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime   

from model.pc.crud import get_logon_pc_percent_by_organization_id, get_pcs_status_by_organization_id

router = APIRouter(
    prefix='/pcs',
    tags=['PC'],
    responses={404: {'description': 'Not found'}},
)

@router.get('/pc_state/{organization_id}/')
def get_pcs_status(
    organization_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    현재 PC의 상태를 조회합니다. 
    """
    try:
        return get_pcs_status_by_organization_id(db, organization_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/get_pc_logon_percent/{organization_id}/')
def get_pc_logon_percent(
    organization_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    특정 조직의 PC 로그인 비율을 조회합니다.
    """
    try:
        logon_percent = get_logon_pc_percent_by_organization_id(db, organization_id)
        return {"logon_percent": logon_percent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))