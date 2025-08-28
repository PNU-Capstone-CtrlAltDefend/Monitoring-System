from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
from model.employee.models import Employees
from datetime import datetime, date

from model.team.models import Teams
from model.department.models import Departments
from model.functional_unit.models import FunctionalUnits
from model.organization.models import Organizations 

def get_or_create_employee(
    db: Session,
    employee_id: str,
    employee_name: str,
    email: str,
    role: str,
    team_id: int,
    wstart: date,
    wend: date,
    supervisor: str = None,
    anomaly_flag: bool = False,
):
    try:
        employee = db.query(Employees).filter(Employees.employee_id == employee_id).first()
        if employee:
            return employee

        employee = Employees(
            employee_id=employee_id,
            employee_name=employee_name,
            email=email,
            role=role,
            team_id=team_id,
            wstart=wstart,
            wend=wend,  
            supervisor=supervisor,
            anomaly_flag=anomaly_flag
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except Exception as e:
        db.rollback()
        raise ValueError(f"An error occurred while creating the employee: {e}") 
    

def get_employees_by_organization_id(db: Session, org_id: uuid.UUID) -> list[Employees]:
    return (
        db.query(Employees)
        .join(Teams, Employees.team_id == Teams.team_id)
        .join(Departments, Teams.department_id == Departments.department_id)
        .join(FunctionalUnits, Departments.functional_unit_id == FunctionalUnits.functional_unit_id)
        .join(Organizations, FunctionalUnits.organization_id == Organizations.organization_id)
        .filter(Organizations.organization_id == org_id)
        .distinct()               # SQL의 DISTINCT 대응
        .all()
    )

def get_employee_id_by_name(db:Session, employee_name:str) -> str | None:
    employee = db.query(Employees).filter(Employees.employee_name == employee_name).first()
    return employee.employee_id if employee else None

def get_anomaly_flag_by_employee_id(db: Session, employee_id: str) -> bool | None:
    employee = db.query(Employees).filter(Employees.employee_id == employee_id).first()
    return employee.anomaly_flag if employee else None