import logging

import psycopg2

logger = logging.getLogger(__name__)


def _daycount(site='test', tag='', searchbody=''):
	from psycopg2.extras import DictCursor
	from niascape import ini
	con = ini['postgresql'].get('connect')

	logger.debug(con)
	
	tagwhere = ''
	bodywhere = ''

	# fixme プレースホルダ使う

	if tag != '':
		tagwhere = f"AND (tags like '% {tag} %' or tags like '% {tag}:%')"
	elif searchbody != '':
		bodywhere = f"AND body LIKE '%{searchbody}%'"

	sql = f"""
	SELECT
		to_char(DATE("datetime"),'YYYY-MM-DD') as "Date" ,
		COUNT(*)                               as "count"
	FROM basedata
	WHERE site = '{site}'
		{tagwhere}
		{bodywhere}
	GROUP BY DATE("datetime")
	ORDER BY DATE("datetime") DESC
	LIMIT 400
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


if __name__ == '__main__':  # pragma: no cover
	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	print(_daycount('test', '#test'))
