from fastapi import FastAPI
from helpers.parser import Parser
from client.consumer import Consumer
from database.connection import Connection
import os

class App (FastAPI):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		config = Parser.parse_config('configs/config_client.json', ['host', 'port', 'login', 'password'])
		if config is None:
			return
		self.client = Consumer(self.log_incoming_message, config)
		self.db_connection = Connection()

	def log_incoming_message(self, message: dict):
		print('Here we got incoming message ', message)
		self.db_connection.insert(message)

	def close(self):
		self.db_connection.close()
