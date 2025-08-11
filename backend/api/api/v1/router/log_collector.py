from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import json

from model.database import get_db

from model.behavior_log import schemas as behavior_log_schemas
from model.behavior_log import crud as behavior_log_crud

router = APIRouter(
    prefix="/log_collector",
    tags=["Log Collector"],
    responses={404: {"description": "Not found"}},
)

@router.post("/post_log")
async def post_behavior_log(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Fluentd/Agent로부터 JSON 로그를 받아서 DB에 저장
    """
    try:
        raw_data = await request.body()

        try:
            data_dict = json.loads(raw_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")

        log_data = behavior_log_schemas.BehaviorLogCreate(**data_dict)
        new_log = behavior_log_crud.create_behavior_log(db, log_data)
        
        return {"msg": "로그가 성공적으로 저장되었습니다.", "event_id": new_log.event_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
