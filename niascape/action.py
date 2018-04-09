import json

import niascape
from niascape.entity import basedata
from niascape.utility.database import get_db
from niascape.utility.json import AsdictSupportJSONEncoder


# noinspection PyUnusedLocal
def top(option: dict) -> str:  # PENDING topという概念はWebでしか無いのでは であればwsgiclientで実装すべきでは
	return 'top'


def daycount(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata._daycount(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def tagcount(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata._tag_count(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか

def timeline(option):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata.get_all(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか

