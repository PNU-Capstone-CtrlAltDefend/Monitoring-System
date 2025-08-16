from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
from model.employee.models import Employees
from datetime import datetime, date

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