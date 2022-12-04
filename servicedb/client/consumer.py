import aio_pika
import json

class Consumer:
  def __init__ (self, process_callable, config):
    self.process_callable = process_callable
    self.host = config["host"]
    self.port = config["port"]
    self.login = config["login"]
    self.password = config["password"]
    self.queue = config["queue"]
  
  async def process_incoming_message(self, message):
      await message.ack()
      body = message.body
      if body:
        str = body.decode('utf-8')
        appeal = json.loads(str)
        self.process_callable(appeal)

  async def consume(self, loop):
    connection = await aio_pika.connect_robust(host=self.host,
                                      port=self.port,
                                      loop=loop,
                                      login=self.login,
                                      password=self.password)                                  
    channel = await connection.channel()
    queue = await channel.declare_queue(self.queue)
    await queue.consume(self.process_incoming_message, no_ack=False)
    return connection