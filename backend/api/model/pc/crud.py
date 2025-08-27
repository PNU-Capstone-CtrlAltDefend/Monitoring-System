# crud.py
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from model.pc.models import Pcs, LogonState
from model.pc.schemas import PcsCreate


def create_pc(db: Session, pc_data: PcsCreate) -> Pcs:
    if get_pc_by_id(db, pc_data.pc_id):
        return
    
    new_pc = Pcs(**pc_data.dict())
    db.add(new_pc)
    try:
        db.commit()
        db.refresh(new_pc)
        return new_pc
    except IntegrityError:
        db.rollback()
        raise ValueError("PC with same IP or MAC address already exists")
    

def get_pcs_by_organization_id(db: Session, organization_id: uuid.UUID) -> list[Pcs]:
    return db.query(Pcs).filter(Pcs.organization_id == organization_id).all()

def get_pc_by_id(db: Session, pc_id: str) -> Pcs | None:
    return db.query(Pcs).filter(Pcs.pc_id == pc_id).first()

def set_pc_current_state_and_present_user_id_by_pc_id(db: Session, pc_id: str, current_state: LogonState, present_user_id: str):
    pc = get_pc_by_id(db, pc_id)
    if not pc:
        return None
    pc.current_state = current_state
    pc.present_user_id = present_user_id
    db.commit()
    db.refresh(pc)
    return pc

def set_pc_access_flag_by_id(db: Session, pc_id: str, access_flag: bool):
    pc = get_pc_by_id(db, pc_id)
    if not pc:
        return None
    pc.access_flag = access_flag
    db.commit()
    db.refresh(pc)
    return pc

def get_ip_and_mac_address_by_id(db:Session, pc_id: str) -> tuple[str | None, str | None] | None:
    pc = get_pc_by_id(db, pc_id)
    if not pc:
        return None
    return (pc.ip_address, pc.mac_address)