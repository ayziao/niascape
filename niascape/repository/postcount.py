"""
niascape.repository.postcount

投稿件数リポジトリ

"""
from typing import List, Dict, Union, Any, NamedTuple

from niascape.utility.database import Database
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)


# noinspection PyShadowingNames
def day(db: Database, site: str = 'test', tag: str = '', search_body: str = '') -> List[Any]:
	"""
	戻り値 名前付きタプルのリスト # xxx List[DayCount] するにはclass DayCount(NamedTuple) 必要 pypy…
	"""
	tag_where = ''
	body_where = ''
	param = [site]  # type: List[Union[str, int]]

	if tag != '':
		tag_where = "AND (tags like ? or tags like ?)"
		param.extend([f"% {tag} %", f"% {tag}:%"])
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
	day_count = NamedTuple('day_count', (('date', str), ('count', int)))
	logger.debug("日付投稿数SQL: %s", sql)
	logger.debug("プレースホルダパラメータ: %s", param)

	return db.execute_fetchall(sql, param, namedtuple=day_count)


# noinspection PyShadowingNames
def month(db: Database, site: str = 'test', tag: str = '', search_body: str = '') -> List[Any]:
	tag_where = ''
	body_where = ''
	param = [site]  # type: List[Union[str, int]]

	if tag != '':
		tag_where = "AND (tags like ? or tags like ?)"
		param.extend([f"% {tag} %", f"% {tag}:%"])
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
	ORDER BY {date}
	LIMIT ?
	"""
	limit = 1000  # PENDING ページングする？
	param.append(limit)
	month_count = NamedTuple('month_count', (('date', str), ('count', int)))

	return db.execute_fetchall(sql, param, namedtuple=month_count)


def hour(db: Database, site: str = 'test', tag: str = '', search_body: str = '', past='') -> List[Any]:
	tag_where = ''
	body_where = ''
	past_where = ''
	dt = datetime.now()
	param = [site]  # type: List[Union[str, int]]

	# FIXME やっつけ
	if tag != '':
		tag_where = "AND (tags like ? or tags like ?)"
		param.extend([f"% {tag} %", f"% {tag}:%"])
	if search_body != '':
		body_where = "AND body LIKE ?"
		param.append(f"%{search_body}%")
	if past == '24H':
		if db.dbms == 'postgresql':
			dt -= timedelta(days=1)
			past_where = 'AND "datetime" > ' + "'" + dt.strftime("%Y-%m-%d %H:%M:%S") + "'"
		else:
			past_where = 'AND "datetime" > ' + "datetime('" +dt.strftime("%Y-%m-%d %H:%M:%S") +  "', '-24 hours')"
	if past == '7D':
		if db.dbms == 'postgresql':
			dt -= timedelta(days=7)
			past_where = 'AND "datetime" > ' + "'" + dt.strftime("%Y-%m-%d %H:%M:%S") + "'"
		else:
			past_where = 'AND "datetime" > ' + "datetime('" + dt.strftime("%Y-%m-%d %H:%M:%S") + "', '-7 days')"
	if past == '30D':
		if db.dbms == 'postgresql':
			dt -= timedelta(days=30)
			past_where = 'AND "datetime" > ' + "'" + dt.strftime("%Y-%m-%d %H:%M:%S") + "'"
		else:
			past_where = 'AND "datetime" > ' + "datetime('" + dt.strftime("%Y-%m-%d %H:%M:%S") + "', '-30 days')"
	if past == '365D':
		if db.dbms == 'postgresql':
			dt -= timedelta(days=365)
			past_where = 'AND "datetime" > ' + "'" + dt.strftime("%Y-%m-%d %H:%M:%S") + "'"
		else:
			past_where = 'AND "datetime" > ' + "datetime('" + dt.strftime("%Y-%m-%d %H:%M:%S") + "', '-365 days')"

	if db.dbms == 'postgresql':
		date = 'to_char("datetime",\'HH24\')'
	else:
		date = 'strftime(\'%H\',"datetime")'

	sql = f"""
	SELECT 
		{date} as "date",
		COUNT(*) as "count"
	FROM basedata
	WHERE site = ?
		{tag_where}
		{body_where}
		{past_where}
	GROUP BY {date}
	ORDER BY {date}
	"""
	hour_count = NamedTuple('hour_count', (('date', str), ('count', int)))

	ret = db.execute_fetchall(sql, param, namedtuple=hour_count)

	# logger.debug("期間 :%s", past)
	# logger.debug("開始日時 :%s", dt)
	# logger.debug(ret)
	# logger.debug(site)
	# logger.debug(sql)

	ret24 = []

	for i in range(24):
		h = '{0:02d}'.format(i)
		if len(ret) > 0 and ret[0].date == h:
			ret24.append(ret.pop(0))
		else:
			ret24.append(hour_count(h, 0))

	return ret24


def tag(db: Database, site: str = 'test') -> List[Dict[str, Union[str, int]]]:
	# PENDING ShadowingNamesに対応すべきかどうか
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
	tag_count = NamedTuple('tag_count', (('tags', str), ('count', int)))

	namedtuple_result = db.execute_fetchall(sql, (site,), namedtuple=tag_count)

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
