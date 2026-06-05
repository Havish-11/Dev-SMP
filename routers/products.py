from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["products"])

class Product(BaseModel):
    id: int
    name: str
    price: float

products_db = []

@router.get("/products", response_model=List[Product])
def get_products():
    return products_db

@router.get("/products/{id}", response_model=Product)
def get_product(id: int):
    product = next((p for p in products_db if p.id == id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=Product)
def create_product(product: Product):
    products_db.append(product)
    return product

@router.put("/products/{id}", response_model=Product)
def update_product(id: int, updated_product: Product):
    for index, p in enumerate(products_db):
        if p.id == id:
            products_db[index] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/products/{id}")
def delete_product(id: int):
    for index, p in enumerate(products_db):
        if p.id == id:
            products_db.pop(index)
            return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")