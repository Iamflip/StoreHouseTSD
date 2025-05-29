from pydantic import BaseModel

class ProductDto(BaseModel):
    product_rid: int
    quantity: int
    product_name: str = None