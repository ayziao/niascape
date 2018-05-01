import json

import niascape
from niascape.repository import basedata
from niascape.utility.database import get_db
from niascape.utility.json import AsdictSupportJSONEncoder


def day(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata._daycount(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def month(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(basedata._monthcount(db, **option), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか
