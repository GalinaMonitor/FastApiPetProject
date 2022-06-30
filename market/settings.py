from pydantic import BaseSettings


class Settings(BaseSettings):
	server_host: str = '0.0.0.0'
	server_port: int = 8000
	database_url: str = 'postgresql+asyncpg://market:8A5uiMoHcHBGBpDQwfmG@localhost:5432/market_db'


settings = Settings(
	_env_file='.env',
	_env_file_encoding='utf-8',
)