import jwt
from fastapi import HTTPException, Depends, status
from datetime import datetime, timedelta
from utils import resources
from utils.auth import oauth2_scheme
from cryptography.fernet import Fernet
from repository import shRepo
from dto.loginDto import LoginDto
from utils.api_response import APIResponse

key = Fernet.generate_key()
cipher = Fernet(key)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=10000)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, resources.SECRET_KEY, algorithm=resources.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, resources.SECRET_KEY, algorithms=[resources.ALGORITHM],
                             options={"verify_exp": True})

        # Извлекаем данные из payload
        username = payload.get("username")
        encrypted_password = payload.get("password")
        exp = payload.get("exp")  # Получаем время истечения срока действия токена

        # Проверяем, не истёк ли токен
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if username is None or encrypted_password is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Расшифровываем пароль
        decrypted_pas = cipher.decrypt(encrypted_password.encode()).decode()

        # Проверяем пользователя через внешний сервис
        access = shRepo.login(LoginDto(login=username, password=decrypted_pas)).json()['errorCode']

        if access == 1:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return {'login': username, 'password': decrypted_pas}  # Возвращаем пользователя для использования в других эндпоинтах

    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


def login(login_dto: LoginDto):
    response = shRepo.login(login_dto)
    data = response.json()

    if data['errorCode'] == 1:
        return APIResponse(code=400, message=data['errMessage'])
    else:
        encrypted_pas = cipher.encrypt(login_dto.password.encode())  # Шифруем строку пароля
        user_data = {"username": login_dto.login, "password": encrypted_pas.decode()}  # Сохраняем зашифрованную строку
        token = create_access_token(user_data)
        return APIResponse(code=200, message=data['errMessage'], data=token)
