from typing import List

import psycopg2

import logging

logger = logging.getLogger(__name__)


def _daycount(site: str = 'test', tag: str = '', search_body: str = '') -> List[dict]:
	logger.debug(search_body)

	from psycopg2.extras import DictCursor
	from niascape import ini
	con = ini['postgresql'].get('connect')

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


def tag_count():
	pass


if __name__ == '__main__':  # pragma: no cover
	from pprint import pformat

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	# print(pformat(_daycount('test', '#test')))

	# print(pformat(_daycount(**{'site':'test','tag':'#test','search_body':'test'})))
	print(pformat(_daycount('test', **{'tag': '#test', 'search_body': 'test'})))
