from pydantic import BaseModel

class LoginDto(BaseModel):
    login: str
    password: str
