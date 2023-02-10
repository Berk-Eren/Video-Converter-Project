import pika


channel = None


def get_channel():
    global channel

    if channel == None:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()

    return channel
