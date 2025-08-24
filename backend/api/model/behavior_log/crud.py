from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from model.behavior_log.models import Behavior_logs, Http_logs, Email_logs, Device_logs, Logon_logs, File_logs
from model.behavior_log.schemas import BehaviorLogCreate, HttpLogCreate, EmailLogCreate, DeviceLogCreate, LogonLogCreate, FileLogCreate
from typing import Optional , List, Tuple, Iterable

def create_behavior_log(db: Session, log_data: BehaviorLogCreate) -> Behavior_logs:
    # 1. 공통 로그 저장
    base_log = Behavior_logs(
        event_id = log_data.event_id,
        employee_id=log_data.employee_id,
        pc_id=log_data.pc_id,
        timestamp=log_data.timestamp,
        event_type=log_data.event_type
    )
    db.add(base_log)
    db.commit()
    db.refresh(base_log)

    # 2. event_type에 따라 세부 테이블 저장
    if log_data.event_type == "http":
        db.add(Http_logs(event_id=base_log.event_id, url=log_data.url))

    elif log_data.event_type == "email":
        db.add(Email_logs(
            event_id=base_log.event_id,
            to=log_data.to,
            cc=log_data.cc,
            bcc=log_data.bcc,
            from_addr=log_data.from_addr,
            size=log_data.size,
            attachment=log_data.attachment
        ))
    
    elif log_data.event_type == "device":
        db.add(Device_logs(event_id=base_log.event_id, activity=log_data.activity))

    elif log_data.event_type == "logon":
        db.add(Logon_logs(event_id=base_log.event_id, activity=log_data.activity))

    elif log_data.event_type == "file":
        db.add(File_logs(event_id=base_log.event_id, filename=log_data.filename))

    db.commit()
    return base_log

def get_all_behavior_logs(db: Session):
    return db.query(Behavior_logs).all()

def get_behavior_logs_by_event_id(db: Session, event_id: str) -> List[Behavior_logs]:
    return db.query(Behavior_logs).filter(Behavior_logs.event_id == event_id).all()

def get_behavior_logs_by_employee_id(db: Session, employee_id: str) -> List[Behavior_logs]:
    return db.query(Behavior_logs).filter(Behavior_logs.employee_id == employee_id).all()

def get_behavior_logs_by_event_type(db: Session, event_type: str) -> List[Behavior_logs]:
    return db.query(Behavior_logs).filter(Behavior_logs.event_type == event_type).all()

def get_behavior_logs_by_period(db: Session, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> List[Behavior_logs]:
    query = db.query(Behavior_logs)

    if start_time and end_time:
        query = query.filter(Behavior_logs.timestamp.between(start_time, end_time))
    elif start_time:
        query = query.filter(Behavior_logs.timestamp >= start_time)
    elif end_time:
        query = query.filter(Behavior_logs.timestamp <= end_time)
    
    return query.order_by(Behavior_logs.timestamp.desc()).all()

def get_logon_logs_by_event_ids(db: Session, event_ids: list[str]) -> list[Logon_logs]:
    return db.query(Logon_logs).filter(Logon_logs.event_id.in_(event_ids)).all()

def get_http_logs_by_event_ids(db: Session, event_ids: list[str]) -> list[Http_logs]:
    return db.query(Http_logs).filter(Http_logs.event_id.in_(event_ids)).all()

def get_email_logs_by_event_ids(db: Session, event_ids: list[str]) -> list[Email_logs]:
    return db.query(Email_logs).filter(Email_logs.event_id.in_(event_ids)).all()

def get_device_logs_by_event_ids(db: Session, event_ids: list[str]) -> list[Device_logs]:
    return db.query(Device_logs).filter(Device_logs.event_id.in_(event_ids)).all()

def get_file_logs_by_event_ids(db: Session, event_ids: list[str]) -> list[File_logs]:
    return db.query(File_logs).filter(File_logs.event_id.in_(event_ids)).all()