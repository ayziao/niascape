from typing import List

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


def _tag_count(site: str = 'test'):
	con = niascape.ini['postgresql'].get('connect')

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

	with psycopg2.connect(con) as conn:
		with conn.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql)
			rows = cur.fetchall()

			dict_result = []
			for row in rows:
				dict_result.append(dict(row))

	aaa = {}
	for bbb in dict_result:
		tags = bbb['tags'].strip().replace('\t',' ').split(' ')
		for ccc in tags:
			if ccc in aaa.keys() :
				aaa[ccc] += bbb['count']
			else:
				aaa[ccc] = bbb['count']

	result = []
	for k, v in sorted(aaa.items(), key=lambda x: -x[1]):
		result.append({'tag':k,'count':v})
	
	return result


if __name__ == '__main__':  # pragma: no cover
	from pprint import pprint

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	# pprint(_daycount('test', '#test')))

	# pprint(_daycount(**{'site':'test','tag':'#test','search_body':'test'}))
	# pprint(_daycount('test', **{'tag': '#test', 'search_body': 'test'}))
	# pprint(_daycount('test', **{'tag': '#test'}))
	pprint(_tag_count(''))
