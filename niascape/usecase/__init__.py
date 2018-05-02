import json

import niascape
from niascape.repository import basedata
from niascape.utility.database import get_db
from niascape.utility.json import AsdictSupportJSONEncoder


# noinspection PyUnusedLocal
def top(option: dict) -> str:  # PENDING topという概念はWebでしか無いのでは であればwsgiclientで実装すべきでは
	return 'top'


def sites(option: dict) -> str:
	# PENDING サイトを取りまとめるパッケージ下に入れるか検討
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata._sites(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def timeline(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata.get_all(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか

# TODO とりあえず試作を移植
