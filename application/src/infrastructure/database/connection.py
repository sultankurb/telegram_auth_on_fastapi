from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config.config import settings

engine = create_async_engine(url=settings.DATABASE_URL)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
