import os
import sys
import json
from mq import get_channel


def main():
    channel = get_channel()
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        body = body.decode()
        file_ids = json.loads(body)
        print(" [*] The file '%(source)s' is converted to '%(target)s'" % file_ids)

    channel.basic_consume(queue=os.environ.get("MP3_QUEUE"), 
                            on_message_callback=callback, 
                                auto_ack=True )

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(" [*] Closing the notification service")
        sys.exit()
