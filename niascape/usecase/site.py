import json

import niascape
from niascape.repository import site
from niascape.utility.database import get_db
from niascape.utility.json import AsdictSupportJSONEncoder


# noinspection PyShadowingBuiltins
def list(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return json.dumps(site.sites(db), cls=AsdictSupportJSONEncoder)  # PENDING どこでJSON化すべきか


def formbottominsert(option: dict) -> str:  # FIXME ひどい名前
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		ret = site.setting(db, **option)

		if 'siteinsert' in ret:
			siteinsert = ret['siteinsert']
		else:
			siteinsert = ''

		return siteinsert
