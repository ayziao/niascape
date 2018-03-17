import json

from niascape.entity import basedata


def top(option):
	return 'top'


def daycount(option):
	return json.dumps(basedata._daycount(option[0], option[1], option[2]))  # PENDING どこでJSON化すべきか
	# return 'daycount'
