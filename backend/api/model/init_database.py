import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from core.config import settings
from model.database import engine, get_db, Base

from model.security_manager import models as SecurityManager_models
from model.security_manager import crud as security_manager_crud
from model.security_manager import schemas as security_manager_schemas


def init_database(engine: engine, db: Annotated[Session, Depends(get_db)]):
    #create all tables
    Base.metadata.create_all(bind=engine)

    # Create Admin User if not exists
    admin_user = security_manager_crud.get_security_manager_by_name(db, settings.ADMIN_USERNAME)
    if not admin_user:
        admin_user = security_manager_schemas.UserCreate(
            manager_id=settings.ADMIN_USERID,
            name=settings.ADMIN_USERNAME,
            organization_name=settings.ADMIN_COMPANY_NAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
        )
        admin_user = security_manager_crud.create_security_manager(db, admin_user)
    # Optionally, you can add initial data here if needed
    # For example, creating an admin user or default security managers
    # This part is usually done in a separate script or during application startup
    print("Database initialized successfully.")