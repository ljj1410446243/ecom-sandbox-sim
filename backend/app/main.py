# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.db import init_db
from app.routers import auth as auth_router
from app.routers import shops as shops_router
from app.routers import products as products_router
from app.routers import listings as listings_router
from app.routers import inventory as inventory_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG,
    version="0.1.0"
)

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动时建表 & 种子用户（仅在没有用户时）
@app.on_event("startup")
def on_startup():
    init_db()
    from app.core.security import get_password_hash
    from app.models.user import User
    from app.core.db import engine
    from sqlmodel import Session, select

    with Session(engine) as session:
        any_user = session.exec(select(User)).first()
        if not any_user:
            demo_users = [
                User(username="teacher1", display_name="Teacher One", email=None,
                     role="teacher", status="active", password_hash=get_password_hash("teacher123")),
                User(username="student1", display_name="Student One", email=None,
                     role="student", status="active", password_hash=get_password_hash("student123")),
            ]
            for u in demo_users:
                session.add(u)
            session.commit()
            print("✅ Seeded demo users: teacher1/teacher123, student1/student123")

# 路由挂载
app.include_router(auth_router.router, prefix=settings.API_PREFIX)
app.include_router(shops_router.router, prefix=settings.API_PREFIX)
app.include_router(products_router.router, prefix=settings.API_PREFIX)
app.include_router(listings_router.router, prefix=settings.API_PREFIX)
app.include_router(inventory_router.router, prefix=settings.API_PREFIX)

# 基础路由
@app.get(f"{settings.API_PREFIX}/health", tags=["system"])
def health():
    return {"status": "ok"}

@app.get(f"{settings.API_PREFIX}/version", tags=["system"])
def version():
    return {"app": settings.APP_NAME, "env": settings.APP_ENV, "debug": settings.APP_DEBUG, "version": "0.1.0"}

@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to EcomSandbox FastAPI backend!"}
