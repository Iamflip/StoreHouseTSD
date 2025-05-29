from dto.loginDto import LoginDto
from repository import shRepo
from utils.api_response import APIResponse


def get_products_by_barcode(barcode: str, login_dto: LoginDto):
    response = shRepo.get_products_by_barcode(barcode, login_dto)
    data = response.json()

    table = data.get('shTable', [])[1]
    headers = table.get('original', [])
    values = table.get('values', [])

    key_values = dict(zip(headers, values))
    temp_products = dict()

    for i in range(len(values[0])):
        product_rid = key_values['1'][i]
        name = key_values['68'][i].rsplit('(', 1)[0].strip()
        temp_products[product_rid] = name

    if temp_products:
        return APIResponse(data=temp_products)
    else:
        return APIResponse(code=404, message='Not Found')