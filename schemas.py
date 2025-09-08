from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class CustomerBase(BaseModel):
    NAME: Optional[str]
    ADDRESS: Optional[str]
    PHONE: Optional[str]
    FAX: Optional[str]
    EMAIL: Optional[str]
    CONTACT_PERSON: Optional[str]
    WEBSITE: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    customerid: int

    class Config:
        # orm_mode = True
        rom_attributes = True
