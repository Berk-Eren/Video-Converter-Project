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

def send_message_to(channel_name, message):
    channel = get_channel()
    channel.queue_declare(queue=channel_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=channel_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
