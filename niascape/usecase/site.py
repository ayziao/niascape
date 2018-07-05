import niascape
from niascape.repository import site
from niascape.utility.database import get_db


# noinspection PyShadowingBuiltins
def list(option: dict) -> list:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return site.sites(db)


def formbottominsert(option: dict) -> dict:  # FIXME ひどい名前
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		ret = site.setting(db, **option)

		if 'siteinsert' in ret:
			siteinsert = ret['siteinsert']
		else:
			siteinsert = ''

		return {'siteinsert': siteinsert}
