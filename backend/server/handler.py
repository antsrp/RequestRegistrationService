import tornado.httpserver
import tornado.web
from service.publisher import Publisher
from helpers.parser import Parser

class EPHandler(tornado.web.RequestHandler):
	def initialize(self, connection):
		self.queue_connection = connection
	def post(self):
		body = self.request.body
		self.queue_connection.send_message(body)
		self.set_status(200)

def create_server(endpoint, connection):
	return tornado.web.Application([
		(endpoint, EPHandler, dict(connection=connection)),
	]
	)