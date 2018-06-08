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
	# FUTURE site別DBにしてsiteカラム削除
	# FUTURE gyazo_posted どうにか

	param = [site]  # type: List[Union[str, int]]

	sql = """
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
	ORDER BY "identifier" DESC
	"""
	param.append("% gyazo_posted %")
	per_page = 200  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)

