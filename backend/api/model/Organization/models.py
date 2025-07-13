from datetime import datetime

from sqlalchemy import Column, BigInteger,  String, Boolean, DateTime
from sqlalchemy.orm import relationship
from model.database import Base

class Organizations(Base):
    __tablename__ = 'organizations'
    organization_id = Column(BigInteger, primary_key=True, index=True)
    organization_name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    security_managers = relationship("Security_managers", back_populates="organization")

    # Relationships
    # Add any relationships if needed