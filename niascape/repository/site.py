"""
niascape.repository.site

サイトリポジトリ
"""
from typing import List, Dict

from niascape.utility.database import Database

import logging

logger = logging.getLogger(__name__)


def sites(db: Database, **option: dict) -> List[Dict[str, int]]:
	sql = """
	SELECT site, COUNT(*) as "count"
	FROM basedata
	GROUP BY site
	ORDER BY COUNT(*) DESC
	"""
	return db.execute_fetchall(sql)


