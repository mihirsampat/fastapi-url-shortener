from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from app.routers.auth import get_current_user
from app.services.url_service import create_url

router = APIRouter(
    prefix="/urls",
    tags=["urls"]
)

@router.post("/", response_model=schemas.URL)
async def create_short_url(
    url: schemas.URLCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new shortened URL"""
    return create_url(db=db, original_url=str(url.original_url), user_id=current_user.id)

@router.get("/", response_model=List[schemas.URL])
async def read_urls(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all URLs for current user"""
    urls = db.query(models.URL).filter(models.URL.user_id == current_user.id)\
        .offset(skip).limit(limit).all()
    return urls

@router.get("/{short_code}", response_model=schemas.URL)
async def read_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get URL details and increment click count"""
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Track click
    url.click_count += 1
    
    # Create click record
    click = models.URLClick(
        url_id=url.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        referer=request.headers.get("referer")
    )
    db.add(click)
    db.commit()
    db.refresh(url)
    
    return url

@router.get("/{short_code}/redirect")
async def redirect_to_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Redirect to original URL"""
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if not url.is_active:
        raise HTTPException(status_code=400, detail="URL is not active")
    
    # Track click
    url.click_count += 1
    
    # Create click record
    click = models.URLClick(
        url_id=url.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        referer=request.headers.get("referer")
    )
    db.add(click)
    db.commit()
    
    return {"url": url.original_url}

@router.delete("/{short_code}", response_model=schemas.URL)
async def delete_url(
    short_code: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a URL"""
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if url.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to delete this URL")
    
    db.delete(url)
    db.commit()
    return url 