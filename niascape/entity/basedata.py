import collections
from typing import List, Dict, Union, Any, NamedTuple

import psycopg2
from psycopg2.extras import DictCursor

import logging

logger = logging.getLogger(__name__)

import niascape


def _daycount(conn, site: str = 'test', tag: str = '', search_body: str = '') -> List[Any]:
	"""
	戻り値 名前付きタプルのリスト # xxx List[Daycount] するにはclass Daycount(NamedTuple) 必要 pypy…
	"""
	# con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
	# logger.debug("接続情報: %s", con)
	# logger.debug(conn) psycopg2.extensions.connection

	tag_where = ''
	body_where = ''

	param = [site]  # type: List[Union[str, int]]

	if tag != '':
		tag_where = "AND (tags like %s or tags like %s)"
		param.extend([f"% {tag} %", f"% {tag}:%"])
	if search_body != '':
		body_where = "AND body LIKE %s"
		param.append(f"%{search_body}%")

	limit = 1000  # PENDING ページングする？
	param.append(limit)

	sql = f"""
	SELECT
		to_char(DATE("datetime"),'YYYY-MM-DD') as "date" ,
		COUNT(*)                               as "count"
	FROM basedata
	WHERE site = %s
		{tag_where}
		{body_where}
	GROUP BY DATE("datetime")
	ORDER BY DATE("datetime") DESC
	LIMIT %s
	"""
	daycount = NamedTuple('daycount', (('date', str), ('count', int)))
	logger.debug("日付投稿数SQL: %s", sql)
	logger.debug("プレースホルダパラメータ: %s", param)

	result = []
	# with psycopg2.connect(con) as conn:
	with conn.cursor(cursor_factory=DictCursor) as cur:
		cur.execute(sql, param)
		for row in cur:
			# result.append(dict(row))
			result.append(daycount(*row))

	return result


def _tag_count(conn, site: str = 'test') -> List[Dict[str, Union[str, int]]]:
	# con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる

	sql = """
	SELECT
		regexp_replace(tags , ':[0-9]+','') as "tags",
		COUNT(*) as "count"
	FROM basedata
	WHERE
		site = %s
	GROUP BY regexp_replace(tags , ':[0-9]+','')
	ORDER BY COUNT(*) DESC
	"""
	tagcount = NamedTuple('tagcount', (('tags', str), ('count', int)))
	namedtuple_result = []  # type: List[Any] # xxx List[Tagcount] するにはclass Tagcount(NamedTuple) 必要 pypy…

	# with psycopg2.connect(con) as conn:
	with conn.cursor(cursor_factory=DictCursor) as cur:
		cur.execute(sql, (site,))
		rows = cur.fetchall()
		# Tagcount = collections.namedtuple('tagcount', list(map(lambda x: x.name, cur.description))) # xxx 動的過ぎてmypyさんにおこられる
		for row in rows:
			namedtuple_result.append(tagcount(*row))

	count_sum = {}  # type: Dict[str, int]
	for row in namedtuple_result:
		tags = row.tags.strip().replace('\t', ' ').split(' ')
		for tag in tags:
			if tag not in count_sum.keys():
				count_sum[tag] = row.count
			else:
				count_sum[tag] += row.count

	result = []  # type:  List[Dict[str, Union[str, int]]]
	for k, v in sorted(count_sum.items(), key=lambda x: -x[1]):
		result.append({'tag': k, 'count': v})

	return result


def get_all(conn, site: str = 'test'):
	limit = 100  # TODO ページング

	# con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
	sql = """
	SELECT * FROM basedata
	WHERE
		site = %s
	ORDER BY "datetime" DESC
	LIMIT %s
	"""
	result = []  # type: List[Any]

	# with psycopg2.connect(con) as conn:
	with conn.cursor(cursor_factory=DictCursor) as cur:
		cur.execute(sql, (site, limit))
		rows = cur.fetchall()
		Item = collections.namedtuple('basedata', list(map(lambda x: x.name, cur.description)))  # xxx 動的過ぎてmypyさんにおこられる
		for row in rows:
			result.append(Item(*row))  # xxx 動的過ぎてmypyさんにおこられる

	return result


if __name__ == '__main__':  # pragma: no cover
	from pprint import pprint

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	# pprint(_daycount('test', '#test')))

	con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる

	with psycopg2.connect(con) as connection:
		# print('aaa')
		# pprint(_daycount(**{'site':'test','tag':'#test','search_body':'test'}))
		pprint(_daycount(connection, 'test', **{'tag': '#test', 'search_body': 'test'}))
		# pprint(_daycount('test', **{'search_body': 'test'}))
		# pprint(_daycount('test', **{'tag': '#test'}))
		pprint(_tag_count(connection, ''))

	# connection.close()

	pprint(get_all(connection))

# for i in res:
# 	pprint(i._asdict())

# import json
# pprint(json.dumps(res))
# pprint(json.dumps(list(map(lambda x:x._asdict(),res))))
