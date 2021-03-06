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


def get(db: Database, identifier: str, site: str = 'test') -> List[Basedata]:
	# FUTURE site別DBにしてsiteカラム削除
	sql = """
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND identifier = ?
	"""
	param = [site, identifier]  # type: List[Union[str, int]]
	return db.execute_fetchone(sql, param, namedtuple=Basedata)


def timeline(db: Database, site: str = 'test', page: int = 1) -> List[Basedata]:
	# FUTURE site別DBにしてsiteカラム削除
	# PENDING gyazo_posted どうにか
	sql = """
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
	ORDER BY "identifier" DESC
	"""
	param = [site, "% gyazo_posted %"]  # type: List[Union[str, int]]
	per_page = 200  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)


def tagtimeline(db: Database, site: str = 'test', tag: str = '', order: str = 'DESC', page: int = 1) -> List[Basedata]:
	# FUTURE site別DBにしてsiteカラム削除
	order = 'ASC' if order == 'ASC' else 'DESC'
	sql = f"""
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND tags LIKE ?
	ORDER BY "identifier" {order}
	"""
	param = [site, f"%#{tag}%"]  # type: List[Union[str, int]]
	per_page = 1000  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)


def search_body(db: Database, site: str = 'test', searchbody: str = '', order: str = 'DESC', page: int = 1) -> List[Basedata]:
	# FUTURE site別DBにしてsiteカラム削除
	order = 'ASC' if order == 'ASC' else 'DESC'
	sql = f"""
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND body LIKE ?
	ORDER BY "identifier" {order}
	"""
	param = [site, f"%{searchbody}%"]  # type: List[Union[str, int]]
	per_page = 1000  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)


def day_timeline(db: Database, site: str = 'test', date: str = '', order: str = 'ASC', page: int = 1) -> List[Basedata]:
	# FUTURE site別DBにしてsiteカラム削除
	# PENDING identifierが YYYYMMDDHHmmSSmmmnnn 形式以外のときは？
	# PENDING dateの妥当性チェック
	order = 'ASC' if order == 'ASC' else 'DESC'
	sql = f"""
	SELECT identifier, title, tags, body, datetime FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
		AND identifier LIKE ?
	ORDER BY "identifier" {order}
	"""
	param = [site, '% gyazo_posted %', f"{date}%"]  # type: List[Union[str, int]]
	per_page = 1000  # FUTURE 1ページあたりの表示数を変更できるようにする
	return db.execute_fetch_page(sql, param, page, per_page, namedtuple=Basedata)


def next_identifier(db: Database, site: str = 'test', date: str = '') -> str:
	# PENDING identifierが YYYYMMDDHHmmSSmmmnnn 形式以外のときは？
	# PENDING dateの妥当性チェック？そもそも identifier 受け取るように？
	sql = f"""
	SELECT identifier FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
		AND identifier > ?
	ORDER BY "identifier" ASC LIMIT 1
	"""
	param = [site, '% gyazo_posted %', f"{date}999999999999"]  # type: List[Union[str, int]]
	ret = db.execute_fetchall_dict(sql, param)

	if len(ret):
		return ret[0]['identifier']
	else:
		return ''


def prev_identifier(db: Database, site: str = 'test', date: str = '') -> str:
	# PENDING identifierが YYYYMMDDHHmmSSmmmnnn 形式以外のときは？
	# PENDING dateの妥当性チェック？そもそも identifier 受け取るように？
	sql = f"""
	SELECT identifier FROM basedata
	WHERE
		site = ?
		AND tags NOT LIKE ?
		AND identifier < ?
	ORDER BY "identifier" DESC LIMIT 1
	"""
	param = [site, '% gyazo_posted %', f"{date}000000000000"]  # type: List[Union[str, int]]
	ret = db.execute_fetchall_dict(sql, param)

	if len(ret):
		return ret[0]['identifier']
	else:
		return ''
