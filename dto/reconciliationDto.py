from pydantic import BaseModel
from dto.productDto import ProductDto
from typing import List, Optional


class ReconciliationDto(BaseModel):
    reconciliation_id: Optional[int] = None
    place_rid: int
    place_name: str
    products: Optional[List[ProductDto]] = None

