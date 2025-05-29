import requests

from dto.reconciliationDto import ReconciliationDto
from utils import resources, payloads
from dto.loginDto import LoginDto

def login(login_dto: LoginDto):
    login_payload = payloads.get_payload_for_login(login_dto)
    return requests.post(resources.ABLE_URL, json=login_payload)

def get_products_by_barcode(barcode: str, login_dto: LoginDto):
    products_by_barcode_payload = payloads.get_payload_by_barcode(barcode, login_dto)
    return requests.post(resources.EXEC_URL, json=products_by_barcode_payload)

def create_reconciliation(reconciliation_dto: ReconciliationDto, login_dto: LoginDto):
    create_reconciliation_payload = payloads.get_payload_for_create_reconciliation(reconciliation_dto, login_dto)
    return requests.post(resources.EXEC_URL, json=create_reconciliation_payload)