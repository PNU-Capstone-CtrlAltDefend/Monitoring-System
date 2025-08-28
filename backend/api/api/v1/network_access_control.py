
from fastapi import APIRouter, Depends, HTTPException, status
from model.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime   

from services.network_controller.pc_access_control_service import NetworkAccessController
from model.pc.crud import set_pc_access_flag_by_id

router = APIRouter(
    prefix='/network_access_control',
    tags=['Network Access Control'],
    responses={404: {'description': 'Not found'}},
)

@router.get('/network-access-control/{organization_id}/{pc_id}/{access_flag}')
def get_pc_logon_percent(
    organization_id: str,
    pc_id: str,
    access_flag: bool, 
    db: Annotated[Session, Depends(get_db)]
):
    """
    특정 조직의 PC 로그인 비율을 조회합니다.
    """
    try:
        networkaccesscontroller = NetworkAccessController(db, pc_id=pc_id, access_flag=access_flag)
        result = networkaccesscontroller.run()
        if result is None or result is False:
            raise HTTPException(status_code=500, detail="접근 제어 실패 ")
        
        set_pc_access_flag_by_id(db, pc_id, access_flag)
        return {"message": "제어 성공"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))