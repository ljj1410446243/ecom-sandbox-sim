from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings


def get_database_url() -> str:
    return (
        f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


engine = create_engine(
    get_database_url(),
    echo=False,  # 调试时可改 True 看 SQL
    pool_pre_ping=True,
    pool_recycle=3600,
)


def init_db() -> None:
    # 导入模型，让 SQLModel 知道表
    from app.models.user import User  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
