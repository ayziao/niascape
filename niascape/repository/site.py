"""
niascape.repository.site

サイトリポジトリ
"""
from typing import List, Dict
import json

from niascape.utility.database import Database

import logging

logger = logging.getLogger(__name__)


def sites(db: Database) -> List[Dict[str, int]]:
	sql = """
	SELECT site, COUNT(*) as "count"
	FROM basedata
	GROUP BY site
	ORDER BY COUNT(*) DESC
	"""
	return db.execute_fetchall(sql)


def setting(db: Database, site: str = 'test') -> dict:
	sql = f"""
	SELECT * FROM keyvalue
	WHERE key = ?
	"""
	logger.log(5, site)

	ret = db.execute_fetchall(sql, ('sitesetting_' + site,))

	logger.log(5, ret)
	logger.log(5, ret[0]['value'])

	return json.loads(ret[0]['value'])
