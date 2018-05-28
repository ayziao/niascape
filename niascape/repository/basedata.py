"""
niascape.repository.basedata

ベースデータリポジトリ
PENDING DBだとかストレージがなにかファイル名にわかるようにつけたほうがよい？
"""
from typing import List

from niascape.utility.database import Database
from niascape.entity.basedata import Basedata

import logging

logger = logging.getLogger(__name__)


def get_all(db: Database, site: str = 'test', page: int = 1) -> List[Basedata]:
	# FIXME site別DBにしてsiteカラム削除
	sql = """
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
	ORDER BY "identifier" DESC
	"""
	per_page = 200  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, (site,), page, per_page, namedtuple=Basedata)
