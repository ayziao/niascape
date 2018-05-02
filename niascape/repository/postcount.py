"""
niascape.repository.postcount

投稿件数リポジトリ

"""
from typing import List, Dict, Union, Any, NamedTuple

from niascape.utility.database import Database

import logging

logger = logging.getLogger(__name__)


def day(db: Database, site: str = 'test', tag_: str = '', search_body: str = '') -> List[Any]:
	"""
	戻り値 名前付きタプルのリスト # xxx List[DayCount] するにはclass DayCount(NamedTuple) 必要 pypy…
	"""
	tag_where = ''
	body_where = ''
	param = [site]  # type: List[Union[str, int]]

	if tag_ != '':
		tag_where = "AND (tags like ? or tags like ?)"
		param.extend([f"% {tag_} %", f"% {tag_}:%"])
	if search_body != '':
		body_where = "AND body LIKE ?"
		param.append(f"%{search_body}%")

	if db.dbms == 'postgresql':
		date = 'to_char(DATE("datetime"),\'YYYY-MM-DD\')'
	else:
		date = 'DATE("datetime")'

	sql = f"""
	SELECT
		{date} as "date" ,
		COUNT(*) as "count"
	FROM basedata
	WHERE site = ?
		{tag_where}
		{body_where}
	GROUP BY DATE("datetime")
	ORDER BY DATE("datetime") DESC
	LIMIT ?
	"""
	limit = 1000  # PENDING ページングする？
	param.append(limit)
	daycount = NamedTuple('daycount', (('date', str), ('count', int)))
	logger.debug("日付投稿数SQL: %s", sql)
	logger.debug("プレースホルダパラメータ: %s", param)

	return db.execute_fetchall(sql, param, namedtuple=daycount)


def month(db: Database, site: str = 'test', tag_: str = '', search_body: str = ''):
	tag_where = ''
	body_where = ''
	param = [site]  # type: List[Union[str, int]]

	if tag_ != '':
		tag_where = "AND (tags like ? or tags like ?)"
		param.extend([f"% {tag_} %", f"% {tag_}:%"])
	if search_body != '':
		body_where = "AND body LIKE ?"
		param.append(f"%{search_body}%")

	if db.dbms == 'postgresql':
		date = 'to_char(DATE("datetime"),\'YYYY-MM\')'
	else:
		date = 'strftime(\'%Y-%m\',"datetime")'

	sql = f"""
	SELECT 
		{date} as "date",
		COUNT(*) as "count"
	FROM basedata
	WHERE site = ?
		{tag_where}
		{body_where}
	GROUP BY {date}
	LIMIT ?
	"""
	limit = 1000  # PENDING ページングする？
	param.append(limit)
	monthcount = NamedTuple('monthcount', (('date', str), ('count', int)))

	return db.execute_fetchall(sql, param, namedtuple=monthcount)


def tag(db: Database, site: str = 'test') -> List[Dict[str, Union[str, int]]]:
	if db.dbms == 'postgresql':
		tags = "regexp_replace(tags , ':[0-9]+','')"
	else:
		tags = "replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(tags,'0',''),'1',''),'2',''),'3',''),'4',''),'5',''),'6',''),'7',''),'8',''),'9',''),':','')"
	sql = f"""
	SELECT
		{tags} as "tags",
		COUNT(*) as "count"
	FROM basedata
	WHERE
		site = ?
	GROUP BY {tags}
	ORDER BY COUNT(*) DESC
	"""
	tagcount = NamedTuple('tagcount', (('tags', str), ('count', int)))

	namedtuple_result = db.execute_fetchall(sql, (site,), namedtuple=tagcount)

	count_sum = {}  # type: Dict[str, int]
	for row in namedtuple_result:
		tags = row.tags.strip().replace('\t', ' ').split(' ')
		for tag_ in tags:
			if tag_ not in count_sum.keys():
				count_sum[tag_] = row.count
			else:
				count_sum[tag_] += row.count

	result = []  # type:  List[Dict[str, Union[str, int]]]
	for k, v in sorted(count_sum.items(), key=lambda x: -x[1]):
		result.append({'tag': k, 'count': v})

	return result