from fastapi import APIRouter
from fastapi.params import Depends
from requests import Session

from dto.loginDto import LoginDto
from dto.productDto import ProductDto
from dto.reconciliationDto import ReconciliationDto
from service import reconciliationService
from service.loginService import get_current_user

from db.database import get_db

router = APIRouter()

@router.post('/reconciliation/create')
def create_reconciliation(reconciliation_dto: ReconciliationDto, user: dict = Depends(get_current_user)):
    return reconciliationService.create_reconciliation(reconciliation_dto, LoginDto(login=user['login'], password=user['password']))


@router.post('/reconciliation/group/create')
def create_group_reconciliation(reconciliation_dto: ReconciliationDto, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return reconciliationService.create_group_reconciliation(reconciliation_dto, db)

@router.get('/reconciliation/group/all/not_uploaded')
def get_all_not_uploaded_reconciliation(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return reconciliationService.get_all_not_uploaded_reconciliation(db)

@router.patch('/reconciliation/group/update/{reconciliation_id}')
def update_reconciliation(reconciliation_id: int, products: list[ProductDto], db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return reconciliationService.update_reconciliation(reconciliation_id, products, db)

@router.patch('/reconciliation/group/upload/{reconciliation_id}')
def upload_reconciliation(reconciliation_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    login_dto = LoginDto(login=user['login'], password=user['password'])
    return reconciliationService.upload_reconciliation(db, reconciliation_id)

@router.get('/reconciliation/group/by_id/{reconciliation_id}')
def get_reconciliation_by_id(reconciliation_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return reconciliationService.get_reconciliation_by_id(db, reconciliation_id)