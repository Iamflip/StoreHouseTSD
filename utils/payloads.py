from dto.loginDto import LoginDto
from dto.reconciliationDto import ReconciliationDto
from utils import operations, resources
from datetime import datetime


def get_payload_for_login(login_dto: LoginDto):
    return {
        'UserName': login_dto.login,
        'Password': login_dto.password,
        'procList': [operations.LOGIN_PROC_NAME]
    }


def get_payload_by_barcode(barcode: str, login_dto: LoginDto):
    return {
        'UserName': login_dto.login,
        'Password': login_dto.password,
        'procName': operations.PROC_NAME_FIND_BY_BARCODE,
        'Input': [
            {'head': 108, 'original': ['4', '5'], 'values': [[barcode], [1]]}
        ]
    }

def get_payload_for_create_reconciliation(reconciliation_dto: ReconciliationDto, login_dto: LoginDto):
    date = datetime.today().strftime("%Y-%m-%d")
    payload = {
    'UserName': login_dto.login,
    'Password': login_dto.password,
    'ProcName': operations.PROC_NAME_CREATE_RECONCILIATION,
    'Input': [
        {'head': 111, 'original': ['33', '31', '105\\1'], 'values': [[resources.ACTIVATED_RECONCILIATION], [date], [reconciliation_dto.place_rid]]}
    ]}

    for product in reconciliation_dto.products:
        product_dict = {'head': 112, 'original': ['210\\1', '210\\206\\1', '32', '31'], 'values': [[product.product_rid], [resources.ONE_PC_RID], [resources.OPTION_ID], [product.quantity]]}
        payload['Input'].append(product_dict)

    return payload

