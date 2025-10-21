from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "EcomSandbox"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:5173"

    DB_USER: str = "ecom_user"
    DB_PASSWORD: str = "MyStrongPassword123"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "my_ecom_sandbox"

    JWT_SECRET: str = "change_this_secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    class Config:
        env_file = ".env"


settings = Settings()
