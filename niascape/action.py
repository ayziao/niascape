import json

from niascape.entity import basedata


def top(option: dict) -> str:
	return 'top'


def daycount(option: dict) -> str:
	return json.dumps(basedata._daycount(**option))  # PENDING どこでJSON化すべきか

def tagcount(option):
	return json.dumps(basedata._tag_count(**option)) # PENDING どこでJSON化すべきか
