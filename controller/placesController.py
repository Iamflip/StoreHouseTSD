from fastapi import APIRouter
from fastapi.params import Depends

import utils.resources
from utils.api_response import APIResponse
from service.loginService import get_current_user

router = APIRouter()

@router.get('/places_list')
def get_places(current_user: str = Depends(get_current_user)):
    return APIResponse(data=utils.resources.PLACES_DICT)