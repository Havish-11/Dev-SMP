from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel, Field

router = APIRouter(prefix="/cart",tags=["cart"])


cart_db = {}

@router.get("/cart")
def get_cart():
    return cart_db

@router.post("/cart/add/{product_id}")
def add_to_cart(product_id: int):
    if product_id in cart_db:
        cart_db[product_id] += 1
    else:
        cart_db[product_id] = 1
    return {"message": "Product added to cart", "cart": cart_db}

@router.delete("/cart/remove/{product_id}")
def remove_from_cart(product_id: int):
    if product_id in cart_db:
        del cart_db[product_id]
        return {"message": "Product removed from cart"}
    raise HTTPException(status_code=404, detail="Product not in cart")
