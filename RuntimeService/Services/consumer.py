import datetime
import json
from Utils import json_util
from dotenv import dotenv_values
import pika
import time
import threading

config = dotenv_values()

class Consumer():
        
    def __init__(self, app, user):
        self.app = app
        self.user = user

    def consume_interval_1(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def consume_interval_2(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def consume_interval_3(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def consume_interval_4(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def consume_interval_5(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def create_consumers(self):
        while True:
            # self.app.rabbit_channel = self.app.rabbit.channel()
            
            # self.app.rabbit_channel.basic_qos(prefetch_count=1)
            
            queue_interval_1 = self.user["user_name"]+"."+config["Symbol"]+"."+config["Interval_1"]
            queue_interval_2 = self.user["user_name"]+"."+config["Symbol"]+"."+config["Interval_2"]
            queue_interval_3 = self.user["user_name"]+"."+config["Symbol"]+"."+config["Interval_3"]
            queue_interval_4 = self.user["user_name"]+"."+config["Symbol"]+"."+config["Interval_4"]
            queue_interval_5 = self.user["user_name"]+"."+config["Symbol"]+"."+config["Interval_5"]

            self.app.rabbit_channel.basic_consume(queue=queue_interval_1, on_message_callback=Consumer.consume_interval_1)
            self.app.rabbit_channel.basic_consume(queue=queue_interval_2, on_message_callback=Consumer.consume_interval_2)
            self.app.rabbit_channel.basic_consume(queue=queue_interval_3, on_message_callback=Consumer.consume_interval_3)
            self.app.rabbit_channel.basic_consume(queue=queue_interval_4, on_message_callback=Consumer.consume_interval_4)
            self.app.rabbit_channel.basic_consume(queue=queue_interval_5, on_message_callback=Consumer.consume_interval_5)

            self.app.rabbit_channel.start_consuming()