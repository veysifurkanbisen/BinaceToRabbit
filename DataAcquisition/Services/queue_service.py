import datetime
import json
from Utils import json_util
from dotenv import dotenv_values
import pika

config = dotenv_values()

class UserQueue():
    credentials = pika.PlainCredentials(config["Rabbit_User"], config["Rabbit_Password"])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            config["Rabbit_Host"],
            config["Rabbit_Port"],
            config["Rabbit_Virtual_Host"],
            credentials
        )
    )
    channel = connection.channel()
    
    
    def __init__(self, user_name, symbol):
        self.user_name = user_name
        self.symbol = symbol
        
    def start_feeding(self, queue):
        queue_dict = {
            "user_name": queue.user_name,
            "symbol": queue.symbol
        }
        json_util.write_json(queue_dict)
        
        now = datetime.datetime.utcnow()
        response = "Started feeding the queues for the user {} at time {} !".format(queue.user_name, now)
        return response

    def stop_feeding(self, user):
        queue_dict = {
            "user_name": user.user_name
        }
        json_util.delete_json(queue_dict)
        
        now = datetime.datetime.utcnow()
        response = "Stoped feeding the queues for the user {} at time {} !".format(user.user_name, now)
        return response

    def feed_queues(self, message, queue_name):       

        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange = '',
            routing_key = queue_name,
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        # print(" [x] Sent %r" % message)


    