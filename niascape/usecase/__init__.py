"""
niascape.usecase

ニアスケイプ基幹ユースケース

"""
import niascape
from niascape.repository import basedata
from niascape.utility.database import get_db


def top(option: dict) -> str:  # PENDING topという概念はWebでしか無いのでは であればwsgiclientで実装すべきでは
	return 'top'


def getdata(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return basedata.get(db, **option)

def timeline(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return basedata.timeline(db, **option)


def tagtimeline(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return basedata.tagtimeline(db, **option)

def day_summary(option: dict):
	site = option['site'] if 'site' in option else 'test'
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		ret = {'content': basedata.day_timeline(db, **option),
					 'next': basedata.next_identifier(db, site, option['date'])[0:8],
					 'prev': basedata.prev_identifier(db, site, option['date'])[0:8]}

		return ret


def searchbody(option: dict):
	with get_db(niascape.ini['database']) as db:  # type: ignore  # XXX セクションぶっこむとmypyさんにおこられ 辞書化すべきか
		return basedata.search_body(db, **option)

#
# FUTURE sarchtitle タイトルの部分検索 PENDING 部分検索は本文とタイトル分けないかオプションにするか
# TODO とりあえず試作を移植 更新系
