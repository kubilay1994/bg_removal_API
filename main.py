from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

from src.api import router as mainRouter



origins = [
    "http://localhost:8080",
]


app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mainRouter, prefix="/api")


@app.get("/api/{all:path}", status_code=404, include_in_schema=False)
def api_not_found():
    raise HTTPException(status_code=404)


@app.get("/{all:path}", include_in_schema=False)
async def index():
    return FileResponse("temp/index.html")
