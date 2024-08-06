from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

try:
    from config import DatabaseConfig as Config
except ImportError:
    from .config import DatabaseConfig as Config
    

Base = declarative_base()


def connection(isolation_level: str = "READ COMMITTED") -> Session:
    engine = create_engine(f"mysql+pymysql://{Config.user}:{Config.password}@{Config.host}:{Config.port}/{Config.name}", isolation_level=isolation_level)
    session = Session(bind=engine)
    return session


def async_connection(isolation_level: str = "READ COMMITTED") -> tuple[Session, Engine]:
    engine = create_async_engine(f"mysql+aiomysql://{Config.user}:{Config.password}@{Config.host}:{Config.port}/{Config.name}", isolation_level=isolation_level)
    session = sessionmaker(bind=engine, class_=AsyncSession)
    return session, engine
