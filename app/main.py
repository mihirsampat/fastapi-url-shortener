from fastapi import FastAPI
from app.routers import auth, urls

app = FastAPI()

app.include_router(auth.router)
app.include_router(urls.router) 