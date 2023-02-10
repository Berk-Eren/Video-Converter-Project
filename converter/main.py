import pika
import json

from mq import get_channel, send_message_to
from db.client import fs
from utils.convert import VideoToMP3Converter


gridfs_example_converter = VideoToMP3Converter(fs)

channel = get_channel()

channel.queue_declare(queue='video_conversion_queue', durable=True)
channel.queue_declare(queue='mp3_queue', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')



def callback(ch, method, properties, body):
    source_file_id = body.decode()
    print(" [x] File id '%s' is received." % source_file_id)
    try:
        gridfs_example_converter.convert_video_to_mp3(source_file_id)
        gridfs_example_converter.save_converted_file_into_db()

        body = {
            "source": source_file_id,
            "target": str(gridfs_example_converter.file_obj)
        }

        send_message_to("mp3_queue", json.dumps(body))

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Done")
    except Exception as e:
        print(" [x] File %s couldn't be converted")
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='video_conversion_queue', 
                        on_message_callback=callback)

channel.start_consuming()
