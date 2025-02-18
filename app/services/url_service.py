import random
import string
from sqlalchemy.orm import Session
from app import models

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_url(db: Session, original_url: str, user_id: int) -> models.URL:
    """Create a new shortened URL"""
    while True:
        short_code = generate_short_code()
        # Check if code already exists
        exists = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        if not exists:
            break
    
    db_url = models.URL(
        original_url=original_url,
        short_code=short_code,
        user_id=user_id
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url 