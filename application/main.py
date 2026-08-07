import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="My api",
    version="0.0.1"
)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
