import os
import pandas as pd 
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from core.config import settings
from model.database import engine, get_db, Base

from model.security_manager import models as SecurityManager_models
from model.security_manager import crud as security_manager_crud
from model.security_manager import schemas as security_manager_schemas

from model.organization import models as Organization_models
from model.organization import crud as organization_crud
from model.organization import schemas as organization_schemas

from model.functional_unit import models as FunctionalUnit_models
from model.functional_unit import crud as functional_unit_crud

from model.department import models as Department_models    
from model.department import crud as department_crud

from model.team import models as Team_models
from model.team import crud as team_crud

from model.employee import models as Employee_models
from model.employee import crud as employee_crud

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

    # 4. 조직 및 직원 데이터 삽입
    csv_file_path = os.path.join(os.path.dirname(__file__), "employee_data.csv")
    df = pd.read_csv(csv_file_path).fillna("")

    for _, row in df.iloc[1:].iterrows():
        # 4-1. 기능 단위 삽입
        if not row["employee_name"]:
            break
        try:
            functional_unit_name = row["functional_unit"]
            functional_unit_name = functional_unit_name.split(" - ")[1]
            functional_unit = functional_unit_crud.get_or_create_functional_unit(
                db, functional_unit_name=functional_unit_name,
                organization_id=organization.organization_id
            )
        except Exception as e:
            print(f"Error creating functional unit: {e}")
            continue    

        # 4-2. 부서 삽입
        if not row["department"]:
            continue
        try:
            department_name = row["department"]
            department_name = department_name.split(" - ")[1]
            department = department_crud.get_or_create_department(
                db, department_name=department_name,
                functional_unit_id=functional_unit.functional_unit_id
            )
        except Exception as e:
            print(f"Error creating department: {e}")
            continue

        # 4-3. 팀 삽입 
        if not row["team"]:
            continue
        try:
            team_name = row["team"]
            team_name = team_name.split(" - ")[1]
            team = team_crud.get_or_create_team(
                db, team_name=team_name,
                department_id=department.department_id
            )
        except Exception as e:
            print(f"Error creating team: {e}")
            continue

        # 4-4. 직원 삽입
        try:
            employee = employee_crud.get_or_create_employee(
                db,
                employee_id=row['user_id'],
                employee_name=row['employee_name'],
                email=row['email'],
                role=row['role'],
                team_id=team.team_id,
                supervisor=row['supervisor'],
                anomaly_flag=False
            )
        except Exception as e:
            print(f"Error creating employee: {e}")
            continue

    print("Database initialized successfully.")