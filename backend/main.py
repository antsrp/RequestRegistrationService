import json
import asyncio

from helpers.parser import Parser
from server.handler import *

async def main():
	config = Parser.parse_config('configs/config_server.json', ['host', 'port', 'endpoint'])
	config_client = Parser.parse_config('configs/config_client.json', ['host', 'port', 'queue', 'user', 'password'])
	if config is None or config_client is None:
		quit()

	connection=Publisher(config_client)
	app = create_server(config["endpoint"], connection)
	app.listen(config["port"])
	await asyncio.Event().wait()

if __name__ == "__main__":
	asyncio.run(main())