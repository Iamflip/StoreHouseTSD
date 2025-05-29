from datetime import datetime

from dto.loginDto import LoginDto
from dto.productDto import ProductDto
from dto.reconciliationDto import ReconciliationDto
from repository import shRepo, reconciliationRepo
from utils.api_response import APIResponse


def create_reconciliation(reconciliation_dto: ReconciliationDto, login_dto: LoginDto):
    response = shRepo.create_reconciliation(reconciliation_dto, login_dto)
    data = response.json()

    print(data)

    if data['errorCode'] == 1:
        return APIResponse(code=400, message=data['errMessage'])
    else:
        return APIResponse(code=200, message=data['errMessage'], data=True)


def create_group_reconciliation(reconciliation_dto: ReconciliationDto, db):
    date = datetime.today().strftime("%Y-%m-%d")
    data = reconciliationRepo.create_reconciliation(db, date, reconciliation_dto.place_rid, reconciliation_dto.place_name, reconciliation_dto.products)

    data = ReconciliationDto(
        reconciliation_id=data.id,
        place_rid=data.place_rid,
        place_name=data.place_name,
        products=[
            ProductDto(
                product_name=p.product_name,
                product_rid=p.product_rid,
                quantity=p.quantity
            ) for p in data.products
        ]
    )

    return APIResponse(data=data)

def get_all_not_uploaded_reconciliation(db):
    data = reconciliationRepo.get_all_reconciliation(db)
    if data:
        data = [ReconciliationDto(
            reconciliation_id=r.id,
            place_rid=r.place_rid,
            place_name=r.place_name,
            products=[
                ProductDto(
                    product_name=p.product_name,
                    product_rid=p.product_rid,
                    quantity=p.quantity
                ) for p in r.products
            ]
        ) for r in data]

        return APIResponse(data=data)
    else:
        return APIResponse(code=404, message="Not Found", data=None)



def update_reconciliation(reconciliation_id, products, db):
    data = reconciliationRepo.update_reconciliation(db, reconciliation_id, products)

    if data:
        data = ReconciliationDto(
            reconciliation_id=data.id,
            place_rid=data.place_rid,
            place_name=data.place_name,
            products=[
                ProductDto(
                    product_name=p.product_name,
                    product_rid=p.product_rid,
                    quantity=p.quantity
                ) for p in data.products
            ]
        )
        return APIResponse(data=data)
    else:
        return APIResponse(code=404, message="Not Found", data=None)

def upload_reconciliation(db, reconciliation_id):
    uploaded_reconciliation = reconciliationRepo.upload_reconciliation(db, reconciliation_id)

    if uploaded_reconciliation:
        return APIResponse(data=uploaded_reconciliation)
    else:
        return APIResponse(code=404, message="Not Found")

def get_reconciliation_by_id(db, reconciliation_id):
    reconciliation_from_db = reconciliationRepo.get_reconciliation_by_id(db, reconciliation_id)
    if reconciliation_from_db:
        reconciliation_dto = ReconciliationDto(
            reconciliation_id=reconciliation_from_db.id,
            place_rid=reconciliation_from_db.place_rid,
            place_name=reconciliation_from_db.place_name,
            products=[
                ProductDto(
                    product_name = p.product_name,
                    product_rid = p.product_rid,
                    quantity = p.quantity
                ) for p in reconciliation_from_db.products
            ]
        )

        return APIResponse(data=reconciliation_dto)
    else:
        return APIResponse(code=404, message="Not Found", data=None)
