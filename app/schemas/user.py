from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import re

class UserOut(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    role: str = Field(..., description="User's role")
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    role: str = Field(..., description="User's role")
    
    @field_validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', v):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
        return v

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")

    model_config = ConfigDict(from_attributes=True)