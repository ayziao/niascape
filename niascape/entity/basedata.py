from typing import List, Dict, Union, Any, NamedTuple

import logging

logger = logging.getLogger(__name__)

from niascape.utility.database import Database


def _daycount(db: Database, site: str = 'test', tag: str = '', search_body: str = '') -> List[Any]:
	"""
	戻り値 名前付きタプルのリスト # xxx List[Daycount] するにはclass Daycount(NamedTuple) 必要 pypy…
	"""
	tag_where = ''
	body_where = ''
	param = [site]  # type: List[Union[str, int]]

	if tag != '':
		tag_where = "AND (tags like %s or tags like %s)"
		param.extend([f"% {tag} %", f"% {tag}:%"])
	if search_body != '':
		body_where = "AND body LIKE %s"
		param.append(f"%{search_body}%")

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
	limit = 1000  # PENDING ページングする？
	param.append(limit)
	daycount = NamedTuple('daycount', (('date', str), ('count', int)))
	logger.debug("日付投稿数SQL: %s", sql)
	logger.debug("プレースホルダパラメータ: %s", param)

	return db.execute_fetchall_namedtuple(sql, param, namedtuple=daycount)


def _tag_count(db: Database, site: str = 'test') -> List[Dict[str, Union[str, int]]]:
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

	namedtuple_result = db.execute_fetchall_namedtuple(sql, (site,), namedtuple=tagcount)

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


def get_all(db: Database, site: str = 'test'):
	sql = """
	SELECT * FROM basedata
	WHERE
		site = %s
	ORDER BY "datetime" DESC
	LIMIT %s
	"""
	limit = 100  # TODO ページング
	return db.execute_fetchall_namedtuple(sql, (site, limit), tuplename='basedata')
