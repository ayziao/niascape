import json

from niascape.entity import basedata


def top(option: dict) -> str:
	return 'top'


def daycount(option: dict) -> str:
	return json.dumps(list(map(lambda x: x._asdict(), basedata._daycount(**option))))  # PENDING どこでJSON化すべきか


def tagcount(option):
	return json.dumps(list(map(lambda x: x._asdict(), basedata._tag_count(**option))))  # PENDING どこでJSON化すべきか
