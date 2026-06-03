from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from database.db import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(String, unique=True, nullable=False)
    organization_name = Column(String, nullable=False)
    organization_type = Column(String, nullable=False)
    official_email = Column(String, unique=True)
    official_mobile = Column(String)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    address = Column(String)
    verification_status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key Relationship
    organization_id = Column(
        String, 
        ForeignKey("organizations.organization_id"), 
        nullable=True
    )

    account_type = Column(String, nullable=False)
    registration_number = Column(String)
    website = Column(String)
    employee_count = Column(Integer, default=0)
    extra_data = Column(String)
    full_name = Column(String, nullable=False)
    designation = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    mobile = Column(String)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="Individual")
    is_active = Column(Boolean, default=True)
    failed_attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
