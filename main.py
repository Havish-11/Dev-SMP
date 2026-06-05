from fastapi import FastAPI
from routers import products, categories, cart, orders

app = FastAPI()

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "API is running"}