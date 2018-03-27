import json

import niascape
from niascape.entity import basedata
from niascape.utility import Database, NamedTupleSupportJSONEncoder


def top(option: dict) -> str:
	return 'top'


def daycount(option: dict) -> str:
	with Database.get_instance(niascape.ini) as db:
		return json.dumps(basedata._daycount(db, **option), cls=NamedTupleSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def tagcount(option):
	with Database.get_instance(niascape.ini) as db:
		return json.dumps(list(map(lambda x: x._asdict(), basedata._tag_count(db, **option))))  # PENDING どこでJSON化すべきか
