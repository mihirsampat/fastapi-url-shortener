from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    urls = relationship("URL", back_populates="owner", cascade="all, delete-orphan")

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=True)
    click_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="urls")
    clicks = relationship("URLClick", back_populates="url", cascade="all, delete-orphan")

class URLClick(Base):
    __tablename__ = "url_clicks"
    
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey("urls.id", ondelete="CASCADE"))
    clicked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ip_address = Column(String(45), nullable=True)  # IPv6 addresses can be up to 45 characters
    user_agent = Column(Text, nullable=True)
    referer = Column(Text, nullable=True)
    country = Column(String(2), nullable=True)
    city = Column(String(100), nullable=True)
    url = relationship("URL", back_populates="clicks") 