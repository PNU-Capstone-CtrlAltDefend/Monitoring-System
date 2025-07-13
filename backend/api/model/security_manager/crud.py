from datetime import datetime

from typing import List, Optional
from core.security import get_password_hash
from sqlalchemy.orm import Session


from . import models, schemas

def get_security_manager_by_name(db: Session, name: str) -> Optional[models.Security_managers]:
    return db.query(models.Security_managers).filter(models.Security_managers.name == name).first()

def get_security_manager_by_id(db: Session, manager_id: str) -> Optional[models.Security_managers]:
    return db.query(models.Security_managers).filter(models.Security_managers.manager_id == manager_id).first()

def create_security_manager(db: Session, security_manager: schemas.UserCreate) -> Optional[schemas.User]:
    db_security_manager = models.Security_managers(
        manager_id=security_manager.manager_id,
        name=security_manager.name,
        organization_name=security_manager.organization_name,
        email=security_manager.email,
        hashed_password=get_password_hash(security_manager.password),  # This should be hashed in a real application
    )
    db.add(db_security_manager)
    db.commit()
    db.refresh(db_security_manager)
    return db_security_manager