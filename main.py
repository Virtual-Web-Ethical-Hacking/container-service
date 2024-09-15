import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.router import router

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/container")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Jalanin aplikasi
if __name__ == "__main__":          # pragma: no cover
    # uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)