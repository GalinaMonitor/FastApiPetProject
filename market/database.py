from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from market.settings import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)


async def get_session() -> AsyncSession:
	async_session = sessionmaker(
		engine,
		class_=AsyncSession,
		autocommit=False,
		autoflush=False
	)
	async with async_session() as session:
		yield session
