import json
import redis
import logging
import pika

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

rds = redis.StrictRedis(host='cache', port=6379, db=0)

connection = pika.BlockingConnection(pika.ConnectionParameters('queue'))
channel = connection.channel()
queue_name = 'test'
channel.queue_declare(queue=queue_name)

def test_func(json_data):
    try:
        logger.info(json_data)
    except Exception as e:
        logger.error(e)

def callback(ch, method, properties, body):
    try:
        json_data = json.loads(body)
        test_func(json_data)
    except Exception as e:
        print(f"Failed to decode JSON message: {e}")
        
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()