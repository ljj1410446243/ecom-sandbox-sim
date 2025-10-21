# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import os


# --------------------------------------------------
# 1. 读取配置 (.env)
# --------------------------------------------------
class Settings(BaseSettings):
    APP_NAME: str = "EcomSandbox"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()


# --------------------------------------------------
# 2. 创建 FastAPI 实例
# --------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG,
    version="0.1.0"
)

# --------------------------------------------------
# 3. 跨域配置 (CORS)
# --------------------------------------------------
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# 4. 挂载路由（后续模块会在这里 import）
# --------------------------------------------------
# from app.routers import auth, shops, rounds  # 示例：未来逐步引入
# app.include_router(auth.router, prefix=settings.API_PREFIX)
# app.include_router(shops.router, prefix=settings.API_PREFIX)
# app.include_router(rounds.router, prefix=settings.API_PREFIX)

# --------------------------------------------------
# 5. 基础路由：健康检查 & 版本信息
# --------------------------------------------------
@app.get(f"{settings.API_PREFIX}/health", tags=["system"])
async def health_check():
    return {"status": "ok"}

@app.get(f"{settings.API_PREFIX}/version", tags=["system"])
async def version_info():
    return {
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "debug": settings.APP_DEBUG,
        "version": "0.1.0"
    }

# --------------------------------------------------
# 6. 根路径（演示）
# --------------------------------------------------
@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to EcomSandbox FastAPI backend!"}
