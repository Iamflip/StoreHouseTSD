from fastapi import APIRouter
from dto.loginDto import LoginDto
from service import loginService

router = APIRouter()

@router.post('/login')
def login(login_dto: LoginDto):
    return loginService.login(login_dto)
