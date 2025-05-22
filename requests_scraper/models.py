from pydantic import BaseModel
from typing import List, Optional

class ProductLink(BaseModel):
    name: str
    url: str
    imageUrl: str
    brandName: str
    price: float
    sellingSize: str
    sku: str
    urlSlugText: str
    keyword: str

    class Config:
        orm_mode = True

class Product(BaseModel):
    itemId: Optional[str] = None
    UPC: Optional[str] = None
    productId: Optional[str] = None
    name: str
    url: str
    image: str
    price: float
    mrp: float
    size: str
    availability: str
    categories: List
    keyword: str
    storeId: Optional[str] = None
    discount: Optional[float] = None
    storeLocation: str 

    class Config:
        orm_mode = True