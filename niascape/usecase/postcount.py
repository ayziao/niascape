"""
niascape.usecase.postcount

投稿件数ユースケース

"""
import niascape
from niascape.repository import postcount
from niascape.utility.database import get_db


def day(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return postcount.day(db, **option)


def month(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return postcount.month(db, **option)


def hour(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return postcount.hour(db, **option)


def week(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return postcount.week(db, **option)


def tag(option: dict) -> str:
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return postcount.tag(db, **option)
