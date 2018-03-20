import json

from niascape.entity import basedata


def top(option):
	return 'top'


def daycount(option):
	return json.dumps(basedata._daycount(**option))  # PENDING どこでJSON化すべきか
