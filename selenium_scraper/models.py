from pydantic import BaseModel
from typing import Optional

class InputGrocery(BaseModel):
    category: str

class GroceryLink(BaseModel):
    link: list

# Grocery
class Grocery(BaseModel):
    itemId: Optional[str]
    UPC: Optional[str]
    productId: Optional[str]
    URL: str
    name: str
    categories: str
    image: str
    storeId: Optional[str | int]
    storeLocation: str
    price: float
    mrp: float
    discount: Optional[str]
    availability: str
    keyword: str
    size: str