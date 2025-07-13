from datetime import datetime

from sqlalchemy import Column, BigInteger,  String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from model.database import Base

class Security_managers(Base):
    __tablename__ = 'security_managers'
    manager_id = Column(String(255), primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    organization_name = Column(String, unique=True, index=True)

    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None)

    # Relationships
    # Add any relationships if needed