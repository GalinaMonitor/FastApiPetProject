from fastapi import FastAPI
from starlette.responses import JSONResponse

from market.api import router
from market.api.error_handler import NotFoundException
from fastapi import Request

app = FastAPI(
	description='Тестовое задание',
	title='Market Open API',
	version='1.0',
)

app.include_router(router)

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
	return JSONResponse(
		status_code=404,
		content=exc.body
	)