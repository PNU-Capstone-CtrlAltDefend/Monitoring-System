# crud.py
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.security import get_auth_code_hash

from model.pc.models import Pcs
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

def get_pc_by_id(db: Session, pc_id: uuid.UUID) -> Pcs | None:
    return db.query(Pcs).filter(Pcs.pc_id == pc_id).first()