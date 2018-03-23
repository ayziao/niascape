import collections
from typing import List, Dict, Union, Any, NamedTuple, Tuple

import psycopg2
from psycopg2.extras import DictCursor

import logging

logger = logging.getLogger(__name__)

import niascape


def _daycount(site: str = 'test', tag: str = '', search_body: str = '') -> List[Any]:
	"""
	戻り値 名前付きタプルのリスト # xxx List[Daycount] するにはclass Daycount(NamedTuple) 必要 pypy…
	"""
	logger.debug(search_body)

	con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる

	logger.debug(con)

	tag_where = ''
	body_where = ''

	param = [site]

	if tag != '':
		tag_where = "AND (tags like %s or tags like %s)"
		param.extend(['% ' + tag + ' %', '% ' + tag + ':%'])
	if search_body != '':
		body_where = "AND body LIKE %s"
		param.append('%' + search_body + '%')

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
	Daycount = NamedTuple('Daycount', (('date', str), ('count', int)))
	logger.debug(sql)
	logger.debug(param)

	with psycopg2.connect(con) as conn:
		with conn.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql, param)
			rows = cur.fetchall()
			result = []
			for row in rows:
				# result.append(dict(row))
				result.append(Daycount(*row))

	return result


def _tag_count(site: str = 'test') -> List[Dict[str, Union[str, int]]]:
	con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる

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
	Tagcount = NamedTuple('Tagcount', (('tags', str), ('count', int)))
	namedtuple_result = []  # type: List[Any] # xxx List[Tagcount] するにはclass Tagcount(NamedTuple) 必要 pypy…

	with psycopg2.connect(con) as conn:
		with conn.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql, (site,))
			rows = cur.fetchall()
			# Tagcount = collections.namedtuple('tagcount', list(map(lambda x: x.name, cur.description))) # xxx 動的過ぎてmypyさんにおこられる
			for row in rows:
				namedtuple_result.append(Tagcount(*row))

	count_sum = {}  # type: Dict[str, int]
	for row in namedtuple_result:
		tags = row.tags.strip().replace('\t', ' ').split(' ')
		for tag in tags:
			if not tag in count_sum.keys():
				count_sum[tag] = row.count
			else:
				count_sum[tag] += row.count

	result = []  # type:  List[Dict[str, Union[str, int]]]
	for k, v in sorted(count_sum.items(), key=lambda x: -x[1]):
		result.append({'tag': k, 'count': v})

	return result


def get_all(site: str = 'test'):
	limit = 100  # TODO ページング

	con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
	sql = """
	SELECT * FROM basedata
	WHERE
		site = %s
	ORDER BY "datetime" DESC
	LIMIT %s
	"""
	result = []  # type: List[Any]

	with psycopg2.connect(con) as conn:
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

	# pprint(_daycount(**{'site':'test','tag':'#test','search_body':'test'}))
	pprint(_daycount('test', **{'tag': '#test', 'search_body': 'test'}))
# pprint(_daycount('test', **{'search_body': 'test'}))
# pprint(_daycount('test', **{'tag': '#test'}))
# pprint(_tag_count(''))

# for i in res:
# 	pprint(i._asdict())

# import json
# pprint(json.dumps(res))
# pprint(json.dumps(list(map(lambda x:x._asdict(),res))))
