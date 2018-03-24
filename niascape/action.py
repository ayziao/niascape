import json

import psycopg2

from niascape.entity import basedata
import niascape


def top(option: dict) -> str:
	return 'top'


def daycount(option: dict) -> str:
	con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
	with psycopg2.connect(con) as conn:
		return json.dumps(list(map(lambda x: x._asdict(), basedata._daycount(conn, **option))))  # PENDING どこでJSON化すべきか


def tagcount(option):
	con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
	with psycopg2.connect(con) as conn:
		return json.dumps(list(map(lambda x: x._asdict(), basedata._tag_count(conn, **option))))  # PENDING どこでJSON化すべきか
