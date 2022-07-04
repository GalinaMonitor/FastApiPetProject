from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from market.settings import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)
async_session = sessionmaker(
	engine,
	class_=AsyncSession,
	autocommit=False,
	autoflush=False
)


async def get_session() -> AsyncSession:
	async with async_session() as session:
		yield session