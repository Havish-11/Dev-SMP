from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel, Field
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

class Order(BaseModel):
    id: int
    items: List[dict]
    total_price: float
    created_at: datetime = Field(default_factory=datetime.now)

orders_db = []

@router.post("/orders", response_model=Order)
def create_order():
    total = 0.0
    items_list = []

    if not cart_db:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for p_id, qty in cart_db.items():
        product = next((p for p in products_db if p.id == p_id), None)
        if product:
            total += (product.price * qty)
            items_list.append({"product_id": p_id, "quantity": qty, "price": product.price})

    new_order = {
        "id": len(orders_db) + 1,
        "items": items_list,
        "total_price": total,
        "created_at": datetime.now()
    }

    orders_db.append(new_order)
    cart_db.clear()
    return new_order

@router.get("/orders", response_model=List[Order])
def get_orders():
    return orders_db

@router.get("/orders/{id}", response_model=Order)
def get_order(id: int):
    order = next((o for o in orders_db if o["id"] == id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order