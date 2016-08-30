import json
import pprint


def getJSON():
	with open("json_idx.json") as f:
		jd = json.load(f)
	return(jd)
	