from fastapi import APIRouter
from fastapi.params import Depends

from dto.loginDto import LoginDto
from service.loginService import get_current_user
from service import productService

router = APIRouter()

@router.get("/products/barcode")
def get_products_by_barcode(barcode: str, user: dict = Depends(get_current_user)):
    return productService.get_products_by_barcode(barcode, LoginDto(login=user['login'], password=user['password']))