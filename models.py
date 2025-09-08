from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime
from database import Base
from datetime import datetime

class TblUser(Base):
    __tablename__ = "tblUser"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    company_id = Column("CompanyId", Integer, nullable=True)
    username = Column("Username", String(100), unique=True)
    password_hash = Column("PasswordHash", Text)
    password_salt = Column("PasswordSalt", Text)
    email = Column("Email", String(254), unique=True)
    role = Column("Role", String(50), nullable=True)
    created_date = Column("CreatedDate", DateTime, default=datetime.utcnow)
    modified_date = Column("ModifiedDate", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TblUserLog(Base):
    __tablename__ = "tblUserLog"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    username = Column("Username", String(100))
    date = Column("Date", Date)
    time = Column("Time", Time)

class Customer(Base):
    __tablename__ = "CUSTOMER"

    customerid = Column(Integer, primary_key=True, autoincrement=True)
    NAME = Column(String(300), nullable=True)
    ADDRESS = Column(String(300), nullable=True)
    PHONE = Column(String(50), nullable=True)
    FAX = Column(String(50), nullable=True)
    EMAIL = Column(String(300), nullable=True)
    CONTACT_PERSON = Column(String(300), nullable=True)
    WEBSITE = Column(String(300), nullable=True)
