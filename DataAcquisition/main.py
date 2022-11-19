from Services.event_loop_service import work as StartLoop
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from Routes.queue_routes import router as queue_router
import asyncio
import threading


settings = {
    "MongoDB_Uri": "mongodb://localhost:27017",
    "DB_Name": "CandleStick"
}

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(settings["MongoDB_Uri"])
    app.database = app.mongodb_client[settings["DB_Name"]]

    thread = threading.Thread(target=lambda: asyncio.run(StartLoop(app)))
    thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()

app.include_router(queue_router, tags=["Queue Operations"], prefix="/queues")



