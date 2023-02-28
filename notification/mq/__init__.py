import os
import pika


channel = None


def get_channel():
    global channel

    if channel == None:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ.get("RABBITMQ_SERVICE_NAME"))
        )
        channel = connection.channel()

    return channel
