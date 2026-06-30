from fastapi import FastAPI
from app.routers import products, sales

app = FastAPI(title="MiniStock API")

app.include_router(products.router)
app.include_router(sales.router)

@app.get("/")
def root():
    return {"message": "MiniStock API is running"}