from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, sales, frozen

app = FastAPI(title="MiniStock API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(sales.router)
app.include_router(frozen.router)

@app.get("/")
def root():
    return {"message": "MiniStock API is running"}