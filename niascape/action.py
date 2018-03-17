import json

from niascape.entity import basedata


def top(option):
	return 'top'


def daycount(option):
	site = option[0] if len(option) > 0 else 'test'
	tag = option[1] if len(option) > 1 else ''
	search_body =  option[2] if len(option) > 2 else ''
	
	return json.dumps(basedata._daycount(site, tag, search_body))  # PENDING どこでJSON化すべきか
	# return 'daycount'
