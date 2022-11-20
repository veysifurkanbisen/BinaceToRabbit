from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from Models.QueueModel import Queue
from Services.queue_service import UserQueue

router = APIRouter()

@router.post("/create_queue", response_description = "Create a new Queue", status_code = status.HTTP_201_CREATED) #response_model = Queue
def create_queue(request: Request, queue: Queue = Body(...)):
    
    user_queue = UserQueue(queue.userName, queue.symbol)

    queue_json = jsonable_encoder(queue)
    result = user_queue.start_feeding(user_queue)

    response = {
        "Status": status.HTTP_200_OK,
        "Message": result,
        "Data": queue_json
    }
    return response

@router.post("/stop_queue", response_description = "Stop an existing Queue", status_code = status.HTTP_201_CREATED) #response_model = Queue
def stop_queue(request: Request, queue: Queue = Body(...)):
    
    user_queue = UserQueue(queue.userName, queue.symbol)
    
    queue_json = jsonable_encoder(queue)
    result = user_queue.stop_feeding(user_queue)

    response = {
        "Status": status.HTTP_200_OK,
        "Message": result,
        "Data": queue_json
    }
    return response
