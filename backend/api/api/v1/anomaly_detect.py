
from fastapi import APIRouter, Depends, HTTPException, status
from model.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime   
from uuid import UUID

from services.anomaly_classification.anomaly_detector import AnomalyDetector
router = APIRouter(
    prefix='/anomalydetect',
    tags=['Anomaly Detect'],
    responses={404: {'description': 'Not found'}},
)

@router.get('/{organization_id}/')
def get_anomaly_detection_results(
    organization_id: str,
    start_dt: datetime,
    end_dt: datetime,
    db: Annotated[Session, Depends(get_db)]
):
    """
    특정 기간 동안의 이상 탐지 결과를 조회합니다.
    date 형식: 
    2010-10-11T00:00:00+00:00
    2010-10-18T00:00:00+00:00
    """
    try:
        anomalydetector = AnomalyDetector(engine, db, start_dt, end_dt, organization_id=UUID(organization_id))
        results = anomalydetector.run()
        print(results)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))