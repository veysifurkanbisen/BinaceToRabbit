from fastapi import FastAPI
from dotenv import dotenv_values
from Services.consumer import Consumer
from Routes.routes import router
from Utils import json_util
import threading
import pika
import asyncio

config = dotenv_values()

app = FastAPI()
@app.on_event("startup")
async def startup_event():
    credentials = pika.PlainCredentials(config["Rabbit_User"], config["Rabbit_Password"])
    # app.rabbit = pika.BlockingConnection(
    #     pika.ConnectionParameters(
    #         config["Rabbit_Host"],
    #         config["Rabbit_Port"],
    #         config["Rabbit_Virtual_Host"],
    #         credentials)
    #     )

    # consumers = []
    # user_list = json_util.read_json()
    # for user in user_list:
    #     consumers.append(Consumer(app, user))

    user_list = json_util.read_json()
    for user in user_list:
        app.rabbit = pika.BlockingConnection(
        pika.ConnectionParameters(
            config["Rabbit_Host"],
            config["Rabbit_Port"],
            config["Rabbit_Virtual_Host"],
            credentials)
        )
        app.rabbit_channel = app.rabbit.channel()
        app.rabbit_channel.basic_qos(prefetch_count=1)
        consumer = Consumer(app, user)
        # threading.Thread(c.create_consumers()).start()
        thread = threading.Thread(target=lambda: asyncio.run(consumer.create_consumers()))
        thread.setName(user["user_name"] + "_" + "consumer_thread")
        thread.setDaemon(True)
        thread.start()



@app.on_event("shutdown")
async def shutdown_event():
    app.rabbit_channel.close()

app.include_router(router, tags=["Live Data Consume"], prefix="/start_live_transfer")