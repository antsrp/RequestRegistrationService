from server.app import App
from helpers.parser import Parser
import uvicorn
import asyncio

config = Parser.parse_config('configs/config_server.json', ['host', 'port'])

app = App()
if config is None or hasattr(app, 'client') is False or hasattr(app, 'db_connection') is False:
	quit()

@app.on_event('startup')
async def startup():
	loop = asyncio.get_running_loop()
	task = loop.create_task(app.client.consume(loop))
	await task

@app.on_event('shutdown')
def shutdown():
	app.close()

if __name__ == "__main__":
	uvicorn.run(app, host=config["host"], port=config["port"])