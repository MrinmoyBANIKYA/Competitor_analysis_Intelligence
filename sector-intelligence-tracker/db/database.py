import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Default to SQLite for local development
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite+aiosqlite:///./test.db"
)

# If DATABASE_URL is for Postgres, ensure it uses the async driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

_initialized = False

async def get_db():
    global _initialized
    if not _initialized:
        # Auto-create all tables in local environments
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        _initialized = True
    async with AsyncSessionLocal() as session:
        yield session
