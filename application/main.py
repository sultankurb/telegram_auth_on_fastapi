import uvicorn
from fastapi import FastAPI
from src.config.config import settings

app = FastAPI(
    title=settings.title,
    description=settings.description,
    version="0.0.1",
    debug=settings.DEBUG,
)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
