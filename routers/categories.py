from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel, Field

router = APIRouter(prefix="/categories", tags=["categories"])

class Category(BaseModel):
    id: int
    name: str

categories_db = []

@router.get("/categories", response_model=List[Category])
def get_categories():
    return categories_db

@router.post("/categories", response_model=Category)
def create_category(category: Category):
    categories_db.append(category)
    return category