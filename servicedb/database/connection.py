import psycopg2
from helpers.parser import Parser

class Connection:
	INSERT_APPEAL = "INSERT INTO appeals (surname, name, patronymic, phone, appeal_text) VALUES ('%s', '%s', '%s', '%s', '%s');"

	def __init__(self):
		config = Parser.parse_config('configs/config_db.json', ['host', 'port', 'database', 'user', 'password'])
		if config is None:
			return
		try:
			self.conn = psycopg2.connect(
				host=config["host"],
				port=config["port"],
				dbname=config["database"],
				user=config["user"],
				password=config["password"]
			)
			if self.conn is None:
				return
			self.cur = self.conn.cursor()
		except Exception as error:
			print("Can't connect to db: ", error)

	def insert(self, appeal):
		try:
			instruction = Connection.INSERT_APPEAL % (appeal["surname"], appeal["name"], appeal["patron"], appeal["phone"], appeal["text_appeal"])
			self.cur.execute(instruction)
			self.conn.commit()
		except Exception as error:
			print("Failed to insert record into appeals table: ", error)

	def close(self):
		if self.cur is not None:
			self.cur.close()
		if self.conn is not None:
			self.conn.close()
		print('Database connection closed.')