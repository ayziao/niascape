from typing import List, Dict, Union, Any

import psycopg2
from psycopg2.extras import DictCursor

import logging

logger = logging.getLogger(__name__)

import niascape


def _daycount(site: str = 'test', tag: str = '', search_body: str = '') -> List[dict]:
	logger.debug(search_body)

	con = niascape.ini['postgresql'].get('connect')

	logger.debug(con)

	tag_where = ''
	body_where = ''

	# fixme プレースホルダ使う

	if tag != '':
		tag_where = f"AND (tags like '% {tag} %' or tags like '% {tag}:%')"
	if search_body != '':
		body_where = f"AND body LIKE '%{search_body}%'"

	sql = f"""
	SELECT
		to_char(DATE("datetime"),'YYYY-MM-DD') as "Date" ,
		COUNT(*)                               as "count"
	FROM basedata
	WHERE site = '{site}'
		{tag_where}
		{body_where}
	GROUP BY DATE("datetime")
	ORDER BY DATE("datetime") DESC
	LIMIT 1000
	"""
	logger.debug(sql)

	with psycopg2.connect(con) as conn:
		with conn.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql)
			rows = cur.fetchall()

			dict_result = []
			for row in rows:
				dict_result.append(dict(row))

	return dict_result


def _tag_count(site: str = 'test') -> List[Dict[str, Union[str, int]]]:
	con = niascape.ini['postgresql'].get('connect')

	# fixme プレースホルダ使う
	sql = f"""
	SELECT
		regexp_replace(tags , ':[0-9]+','') as "tags",
		COUNT(*) as "count"
	FROM basedata
	WHERE
		site = '{site}'
	GROUP BY regexp_replace(tags , ':[0-9]+','')
	ORDER BY COUNT(*) DESC
	"""

	dict_result = []  # type: List[Dict[str, Any]] # XXX List[Dict[str, Union[str, int]]]にしたい 数値にストリップねえよ言われる
	with psycopg2.connect(con) as conn:
		with conn.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql)
			rows = cur.fetchall()

			for row in rows:
				dict_result.append(dict(row)) # PENDING 辞書じゃなくて名前付きタプルにする？

	count_sum = {}  # type: Dict[str, int]
	for row in dict_result:
		tags = row['tags'].strip().replace('\t', ' ').split(' ')
		for tag in tags:
			if not tag in count_sum.keys():
				count_sum[tag] = row['count']
			else:
				count_sum[tag] += row['count']

	result = []  # type:  List[Dict[str, Union[str, int]]]
	for k, v in sorted(count_sum.items(), key=lambda x: -x[1]):
		result.append({'tag': k, 'count': v})

	return result


if __name__ == '__main__':  # pragma: no cover
	from pprint import pprint

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	# pprint(_daycount('test', '#test')))

	# pprint(_daycount(**{'site':'test','tag':'#test','search_body':'test'}))
	# pprint(_daycount('test', **{'tag': '#test', 'search_body': 'test'}))
	# pprint(_daycount('test', **{'tag': '#test'}))
	pprint(_tag_count(''))
