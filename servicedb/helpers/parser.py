import json

class Parser:
	Option_Not_Found = "Error: no option '%s' in config file %s!"
	def parse_config(name, must_have_fields):
		try:
			with open(name) as f:
				config = json.load(f)

		except IOError:
			ptrn = "Error: config of application {name:} wasn't found!"
			print(ptrn.format(name=name))
			return None
	
		for field in must_have_fields:
			if not field in config:
				print(Parser.Option_Not_Found % (field, name))
				return None

		return config