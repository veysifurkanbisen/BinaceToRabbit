from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from Models.UserModel import User

router = APIRouter()

@router.post("/start_live_transfer", response_description = "Create a new Queue", status_code = status.HTTP_201_CREATED)
def start_live_data(request: Request, user: User = Body(...)):
    

    user_json = jsonable_encoder(user)
    result = user_json

    response = {
        "Status": status.HTTP_200_OK,
        "Message": result,
        "Data": []
    }
    return response