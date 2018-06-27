from typing import Any, Dict, List, Union, NamedTuple
from configparser import ConfigParser

import sqlite3

try:
	import psycopg2
	from psycopg2.extras import DictCursor
except ImportError:
	psycopg2 = None
	DictCursor = None

import logging
from pprint import pformat

logger = logging.getLogger(__name__)


class Database:
	def __init__(self, setting: ConfigParser = None) -> None:
		logger.log(5, 'Databaseインスタンス 初期化')

		self._setting = setting
		self.dbms = ''  # type: str
		self._connection = None  # type: Any

		self._connect()

	def _connect(self) -> None:
		if self._setting is None:
			self._connection = sqlite3.connect(":memory:")
		else:
			self._connection = sqlite3.connect(self._setting['connect'])  # type: ignore  # XXX 設定をセクションで受け取ってるとmypyさんにおこられ 辞書化すべきか
			logger.log(5, "sqlite3ファイル :%s", pformat(self._setting['connect']))
		logger.debug("sqlite3接続 :%s", pformat(self._connection))
		self.dbms = 'sqlite'
		self._connection.row_factory = sqlite3.Row

	def execute(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> None:
		# PENDING なんか返す？
		if param is None:
			cursor = self._connection.execute(sql)
		else:
			cursor = self._connection.execute(sql, param)
		logger.log(5, "rowcount :%s", cursor.rowcount)
		cursor.close()

	def execute_fetchone(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None, *, namedtuple=None, tuple_name: str = None):
		# FIXME やっつけ
		return self.execute_fetchall(sql, param, namedtuple=namedtuple, tuple_name=tuple_name)[0]

	def execute_fetchall(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None, *, namedtuple=None, tuple_name: str = None):
		if namedtuple is None and tuple_name is None:
			return self.execute_fetchall_dict(sql, param)
		else:
			return self.execute_fetchall_namedtuple(sql, param, namedtuple=namedtuple, tuple_name=tuple_name)

	def execute_fetch_page(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None, page=1, per_page=100, *, namedtuple=None, tuple_name: str = None):
		if not isinstance(page, int) or page < 1:
			page = 1
		offset = per_page * (page - 1)
		sql += f' LIMIT {per_page} OFFSET {offset}'

		if namedtuple is not None or tuple_name is not None:
			return self.execute_fetchall_namedtuple(sql, param, namedtuple=namedtuple, tuple_name=tuple_name)
		else:
			return self.execute_fetchall_dict(sql, param)

	def execute_fetchall_dict(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> List[Dict[str, Any]]:
		if param is None:
			cursor = self._connection.execute(sql)
		else:
			cursor = self._connection.execute(sql, param)
		logger.log(5, "rowcount :%s", cursor.rowcount)

		result = []
		for row in cursor:
			result.append(dict(row))

		cursor.close()

		return result

	def execute_fetchall_namedtuple(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None, *, namedtuple=None, tuple_name: str = 'namedtuple'):
		if param is None:
			cursor = self._connection.execute(sql)
		else:
			cursor = self._connection.execute(sql, param)
		rows = cursor.fetchall()
		if len(rows) == 0:  # XXX 0件のときの処理やっつけ
			return []
		if namedtuple is None:
			namedtuple = NamedTuple(tuple_name, list(map(lambda x: (x, Any), rows[0].keys())))  # type: ignore  # XXX NamedTupleの型チェック無理

		result = []
		for row in rows:
			result.append(namedtuple(*row))  # type: ignore # XXX NamedTupleの型チェック無理

		cursor.close()

		return result

	def close(self) -> None:
		logger.log(5, "接続クローズ :%s", pformat(self._connection))
		self._connection.close()

	def __enter__(self):
		logger.log(5, "with 開始")
		return self

	def __exit__(self, exception_type, exception_value, traceback) -> None:
		self.close()
		logger.log(5, "with 終了")


class Postgresql(Database):

	def _connect(self) -> None:
		logger.log(5, 'Postgresqlインスタンス 初期化')
		self.dbms = 'postgresql'
		self._connection = psycopg2.connect(self._setting['connect'])
		logger.debug("Postgresql接続 :%s", pformat(self._connection))

	def execute(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> None:
		# PENDING なんか返す？
		with self._connection.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql.replace('?', '%s'), param)

		logger.log(5, "sql :%s", sql)
		logger.log(5, "query :%s", cur.query.decode('utf-8'))

	def execute_fetchall_dict(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> List[Dict[str, Any]]:
		result = []
		with self._connection.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql.replace('?', '%s'), param)
			for row in cur:
				result.append(dict(row))

		logger.log(5, "description :%s", pformat(cur.description))
		logger.log(5, "sql :%s", sql)
		logger.log(5, "query :%s", cur.query.decode('utf-8'))

		return result

	def execute_fetchall_namedtuple(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None, *, namedtuple=None, tuple_name: str = 'namedtuple'):
		result = []
		with self._connection.cursor() as cur:
			cur.execute(sql.replace('?', '%s'), param)
			rows = cur.fetchall()
			if namedtuple is None:
				namedtuple = NamedTuple(tuple_name, list(map(lambda x: (x.name, Any), cur.description)))  # type: ignore # XXX NamedTupleの型チェック無理

			for row in rows:
				result.append(namedtuple(*row))  # type: ignore # XXX NamedTupleの型チェック無理

		logger.log(5, "description :%s", pformat(cur.description))
		logger.log(5, "sql :%s", sql)
		logger.log(5, "query :%s", cur.query.decode('utf-8'))

		return result


def get_db(setting: ConfigParser = None) -> Database:
	if setting is not None:
		if setting['dbms'] == 'sqlite':
			return Database(setting)
		elif setting['dbms'] == 'postgresql' and psycopg2 is not None:
			return Postgresql(setting)

	return Database()
