from sqlalchemy import ( 
    Column, Integer, String, Date, Boolean, ForeignKey, DateTime, func
)
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    """All models inherit from this base class"""
    pass

class District(Base):
    """A school district"""
    __tablename__ = "district"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    students = relationship("Student", back_populates="district")

class Student(Base):
    """students record. FERPA would apply to all fields"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    grade_level = Column(Integer, nullable=False)
    district_id = Column(Integer, ForeignKey("district.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    district = relationship("District", back_populates="students")



class User(Base):
    """Application user"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())