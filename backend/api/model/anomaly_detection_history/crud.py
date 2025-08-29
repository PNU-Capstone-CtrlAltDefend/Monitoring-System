from model.anomaly_detection_history import models 
from model.anomaly_detection_history import schemas
from datetime import datetime
from sqlalchemy.orm import Session
import uuid

def create_anomaly_detection_history(db: Session, organization_id: uuid.UUID, results: str, start_date: datetime, end_date: datetime):
    new_history = models.AnomalyDetectionHistories(
        organization_id=organization_id,
        results=results,
        run_timestamp=datetime.utcnow(),
        start_date=start_date,
        end_date=end_date
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history

def get_anomaly_detection_history_by_duration(db: Session, organization_id: uuid.UUID, start_date: datetime, end_date: datetime):
    return db.query(models.AnomalyDetectionHistories).filter(
        models.AnomalyDetectionHistories.organization_id == organization_id,
        models.AnomalyDetectionHistories.start_date >= start_date,
        models.AnomalyDetectionHistories.end_date <= end_date
    ).first()

