import json

import niascape
from niascape.repository import basedata
from niascape.utility.database import get_db
from niascape.utility.json import AsdictSupportJSONEncoder


def top(option: dict) -> str:  # PENDING topという概念はWebでしか無いのでは であればwsgiclientで実装すべきでは
	return 'top'


def getdata(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata.get(db, str(option['identifier']), option['site']), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def timeline(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata.get_all(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def tagtimeline(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata.tagtimeline(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def searchbody(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata.search_body(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def day_summary(option: dict):
	site = option['site'] if 'site' in option else 'test'
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		ret = {'content': basedata.day_summary(db, **option),
					 'next': basedata.next_identifier(db, site, option['date'])[0:8],
					 'prev': basedata.prev_identifier(db, site, option['date'])[0:8]}

		return json.dumps(ret, cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか

# TODO とりあえず試作を移植
