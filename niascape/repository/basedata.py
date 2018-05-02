"""
niascape.repository.basedata

ベースデータリポジトリ
PENDING DBだとかファイル名にわかるようにつけたほうがよい？
"""
from typing import List, Dict, Union, Any, NamedTuple

from niascape.utility.database import Database
from niascape.entity.basedata import Basedata

import logging

logger = logging.getLogger(__name__)


def _sites(db: Database, **option):
	sql = """
	SELECT site, COUNT(*) as "count"
	FROM basedata
	GROUP BY site
	ORDER BY COUNT(*) DESC
	"""
	return db.execute_fetchall(sql)


def get_all(db: Database, site: str = 'test', page=1):
	sql = """
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
	ORDER BY "identifier" DESC
	"""
	per_page = 200  # FUTURE 1ページあたりの表示数を変更できるようにする
	# return db.execute_fetch_page(sql, (site,), page, per_page, tuple_name='basedata')
	return db.execute_fetch_page(sql, (site,), page, per_page, namedtuple=Basedata)