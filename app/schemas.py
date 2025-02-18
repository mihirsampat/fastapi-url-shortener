from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# URL schemas
class URLBase(BaseModel):
    original_url: HttpUrl
    expires_at: Optional[datetime] = None

class URLCreate(URLBase):
    pass

class URL(URLBase):
    id: int
    short_code: str
    created_at: datetime
    updated_at: datetime
    click_count: int
    is_active: bool
    user_id: int

    class Config:
        from_attributes = True

# URL Click schemas
class URLClickBase(BaseModel):
    ip_address: Optional[str]
    user_agent: Optional[str]
    referer: Optional[str]
    country: Optional[str]
    city: Optional[str]

class URLClick(URLClickBase):
    id: int
    url_id: int
    clicked_at: datetime

    class Config:
        from_attributes = True

# Response schemas
class URLResponse(URL):
    clicks: List[URLClick] = [] 