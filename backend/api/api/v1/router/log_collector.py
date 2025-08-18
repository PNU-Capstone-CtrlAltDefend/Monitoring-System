from typing import Annotated, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from pydantic import ValidationError
import logging
import json
from typing import Annotated

#광훈 버전 
# from fastapi import APIRouter, Depends, HTTPException, status, Request
# from sqlalchemy.orm import Session
# import json, secrets, string
# from pydantic import ValidationError

from model.database import get_db

from model.behavior_log import schemas as behavior_log_schemas
from model.behavior_log import crud as behavior_log_crud

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/log_collector",
    tags=["Log Collector"],
    responses={404: {"description": "Not found"}},
)

def _parse_payload(raw: bytes) -> List[Dict[str, Any]]:
    """
    단일 JSON, JSON 배열, NDJSON(줄 단위) 모두 지원.
    0x1D(레코드 구분자)도 줄바꿈으로 정규화.
    """
    if not raw:
        return []

    text = raw.decode("utf-8", errors="replace").replace("\x1D", "\n").strip()

    # 1) 통으로 JSON 파싱 시도 (객체 or 배열)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return [parsed]
        if isinstance(parsed, list):
            return parsed  # 리스트 안에 dict들이 온다고 가정
    except json.JSONDecodeError:
        pass  # NDJSON 가능성으로 진행

    # 2) NDJSON: 줄 단위 파싱
    objs: List[Dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            objs.append(json.loads(line))
        except json.JSONDecodeError as e:
            log.warning("Invalid JSON line: %s | line=%r", e, line[:200])
            raise HTTPException(status_code=400, detail="Invalid JSON (NDJSON line)")
    return objs
# 광훈 버전
# ALNUM_UP = string.ascii_uppercase + string.digits
# def _gen_event_id() -> str:
#     """
#     {XXXX-XXXXXXXX-XXXXXXXX} 패턴의 랜덤 ID 생성
#     """
#     def seg(n: int) -> str:
#         return ''.join(secrets.choice(ALNUM_UP) for _ in range(n))
#     return f'{{{seg(4)}-{seg(8)}-{seg(8)}}}'

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

        # JSON 파싱
        try:
            data_dicts = _parse_payload(raw_data)
        except HTTPException:
            log.warning("Invalid JSON from %s", request.client.host if request.client else "unknown")
            raise

        if not data_dicts:
            raise HTTPException(status_code=400, detail="Empty payload")

        # 스키마 검증
        event_ids: List[int] = []
        for i, rec in enumerate(data_dicts, start=1):
            try:
                log_data = behavior_log_schemas.BehaviorLogCreate(**rec)
            except ValidationError as e:
                log.info("ValidationError (record %d): %s | payload=%s", i, e.errors(), rec)
                raise HTTPException(status_code=400, detail=e.errors())

            # DB 처리
            try:
                new_log = behavior_log_crud.create_behavior_log(db, log_data)
                event_ids.append(new_log.event_id)
            except IntegrityError as e:
                # FK / UNIQUE / NOT NULL 등 무결성 위반
                db.rollback()
                log.exception("IntegrityError (record %d): %s | payload=%s", i, e.orig, rec)
                raise HTTPException(status_code=409, detail=str(e.orig))
            except DataError as e:
                # 타입/길이 초과 등 데이터 문제
                db.rollback()
                log.exception("DataError (record %d): %s | payload=%s", i, e.orig, rec)
                raise HTTPException(status_code=400, detail=str(e.orig))
            except OperationalError:
                # DB 접속/트랜잭션 문제
                db.rollback()
                log.exception("OperationalError (DB unavailable)")
                raise HTTPException(status_code=503, detail="Database unavailable")

        return {"msg": "로그가 성공적으로 저장되었습니다.", "count": len(event_ids), "event_ids": event_ids}

    except Exception:
        raise
    except Exception as e:
        log.exception("Unhandled exception while handling /post_log: %s", e)
        raise HTTPException(status_code=500, detail="Internal error")
    
    # 광훈 버전 
    #     try:
    #         data_dict = json.loads(raw_data)
    #     except json.JSONDecodeError:
    #         raise HTTPException(status_code=400, detail="Invalid JSON")
        
    #     max_attempts = 5
    #     event_id = None
    #     for _ in range(max_attempts):
    #         candidate = _gen_event_id()
    #         if not behavior_log_crud.get_behavior_logs_by_event_id(db, candidate):
    #             event_id = candidate
    #             break
    #     if not event_id:    
    #         raise HTTPException(status_code=500, detail="Failed to allocate unique event_id")
        
    #     data_dict["event_id"] = event_id

    #     try:
    #         log_data = behavior_log_schemas.BehaviorLogCreate(**data_dict)
    #     except ValidationError as e:
    #         raise HTTPException(status_code=422, detail=e.errors())
        
    #     try:
    #         new_log = behavior_log_crud.create_behavior_log(db, log_data)
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
        
    #     return {"msg": "로그가 성공적으로 저장되었습니다.", "event_id": new_log.event_id}
    
    # except Exception as e:
    #     print(f"로그 저장 중 오류 발생: {e}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=str(e)
    #     )
