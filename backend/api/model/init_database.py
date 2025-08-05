import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from core.config import settings
from model.database import engine, get_db, Base

from model.security_manager import models as SecurityManager_models
from model.security_manager import crud as security_manager_crud
from model.security_manager import schemas as security_manager_schemas

from model.Organization import models as Organization_models
from model.Organization import crud as organization_crud
from model.Organization import schemas as organization_schemas

def init_database(engine: engine, db: Annotated[Session, Depends(get_db)]):
    #create all tables
    Base.metadata.create_all(bind=engine)
    # 2. 기본 조직 존재 여부 확인
    organization = organization_crud.get_organization_by_name(db, settings.ADMIN_COMPANY_NAME)
    if not organization:
        organization = organization_crud.create_organization(db, organization_schemas.OrganizationCreate(
            organization_name=settings.ADMIN_COMPANY_NAME,
            authentication_code=settings.ADMIN_AUTH_CODE,
            description=settings.ADMIN_ORGANIZATION_DESCRIPTION
        ))
    
    additional_organization = organization_crud.get_organization_by_name(db, settings.ADDITIONAL_ORGANIZATIONS_NAME)
    if not additional_organization:
        additional_organization = organization_crud.create_organization(db, organization_schemas.OrganizationCreate(
            organization_name=settings.ADDITIONAL_ORGANIZATIONS_NAME,
            authentication_code=settings.ADDITIONAL_ORGANIZATIONS_AUTH_CODE,
            description=settings.ADDITIONAL_ORGANIZATIONS_DESCRIPTION
        ))

    # 3. 관리자 유저 존재 여부 확인
    admin_user = security_manager_crud.get_security_manager_by_name(db, settings.ADMIN_USERNAME)
    if not admin_user:
        admin_user = security_manager_schemas.UserCreate(
            manager_id=settings.ADMIN_USERID,
            name=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
            organization_id=organization.organization_id  
        )
        security_manager_crud.create_security_manager(db, admin_user)

    print("Database initialized successfully.")