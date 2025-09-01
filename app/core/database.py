from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Cargar variables desde .env si existe
load_dotenv()

# Parámetros de base de datos con defaults locales
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "registralo_db")

# URL de conexión asincrónica (asyncpg)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

# Motor asincrónico
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Sesiones asincrónicas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base para modelos SQLAlchemy
Base = declarative_base()

# Dependencia para usar en FastAPI (en endpoints async def)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session