"""
niascape.usecase.postcount

投稿件数ユースケース

"""
import json

import niascape
from niascape.repository import postcount
from niascape.utility.database import get_db
from niascape.utility.json import AsdictSupportJSONEncoder


def day(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(postcount.day(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def month(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(postcount.month(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def hour(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(postcount.hour(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def week(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(postcount.week(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def tag(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(postcount.tag(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか
