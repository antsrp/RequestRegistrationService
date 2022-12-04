import pika
import json

class Publisher:
  def __init__(self, config):
    self.publish_queue_name = config["queue"]
    credentials = pika.PlainCredentials(config["user"], config["password"])
    self.connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=config["host"], port=config["port"],credentials=credentials)
      )
    self.channel = self.connection.channel()
    self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)

  def send_message(self, message):
    self.channel.basic_publish(
        exchange='',
        routing_key=self.publish_queue_name,
        body=message
    )

  def close():
    self.connection.close()