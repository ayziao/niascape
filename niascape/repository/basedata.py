"""
niascape.repository.basedata

ベースデータリポジトリ
PENDING DBだとかストレージがなにかファイル名にわかるようにつけたほうがよい？
"""
from typing import List, Union

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


def tagtimeline(db: Database, site: str = 'test', tag: str = '', order: str = 'DESC', page: int = 1) -> List[Basedata]:
	# FUTURE site別DBにしてsiteカラム削除

	param = [site, f"%#{tag}%"]
	order = 'ASC' if order == 'ASC' else 'DESC'

	sql = f"""
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND tags LIKE ?
	ORDER BY "identifier" {order}
	"""
	per_page = 1000  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)


def search_body(db: Database, site: str = 'test', searchbody: str = '', order: str = 'DESC', page: int = 1) -> List[Basedata]:
	# FUTURE site別DBにしてsiteカラム削除

	param = [site, f"%{searchbody}%"]
	order = 'ASC' if order == 'ASC' else 'DESC'

	sql = f"""
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND body LIKE ?
	ORDER BY "identifier" {order}
	"""
	per_page = 1000  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)


def day_summary(db: Database, site: str = 'test', date: str = '', order: str = 'ASC', page: int = 1) -> List[Basedata]:
	# FIXME メソッド名が実装にあってない
	# FUTURE site別DBにしてsiteカラム削除
	# PENDING identifierが YYYYMMDDHHmmSSmmmnnn 形式以外のときは？
	# PENDING dateの妥当性チェック

	param = [site, '% gyazo_posted %', f"{date}%"]
	order = 'ASC' if order == 'ASC' else 'DESC'

	sql = f"""
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
		AND identifier LIKE ?
	ORDER BY "identifier" {order}
	"""
	per_page = 1000  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)


def next_identifier(db: Database, site: str = 'test', date: str = '') -> str:
	# PENDING identifierが YYYYMMDDHHmmSSmmmnnn 形式以外のときは？
	# PENDING dateの妥当性チェック？そもそも identifier 受け取るように？

	param = [site, '% gyazo_posted %', f"{date}999999999999"]

	sql = f"""
	SELECT identifier FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
		AND identifier > ?
	ORDER BY "identifier" ASC LIMIT 1
	"""

	ret = db.execute_fetchall_dict(sql, param)

	if len(ret):
		return ret[0]['identifier']
	else:
		return ''


def prev_identifier(db: Database, site: str = 'test', date: str = '') -> str:
	# PENDING identifierが YYYYMMDDHHmmSSmmmnnn 形式以外のときは？
	# PENDING dateの妥当性チェック？そもそも identifier 受け取るように？

	param = [site, '% gyazo_posted %', f"{date}000000000000"]

	sql = f"""
	SELECT identifier FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
		AND identifier < ?
	ORDER BY "identifier" DESC LIMIT 1
	"""

	ret = db.execute_fetchall_dict(sql, param)

	if len(ret):
		return ret[0]['identifier']
	else:
		return ''
