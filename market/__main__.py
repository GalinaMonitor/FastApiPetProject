import uvicorn

uvicorn.run(
	"market.app:app",
	reload=True
)
