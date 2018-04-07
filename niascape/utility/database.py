from typing import Any, Dict, List, Union
from configparser import ConfigParser

import collections
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
		logger.debug('Databaseインスタンス 初期化')
		self._setting = setting
		self._connect()

	def _connect(self) -> None:
		if self._setting is None:
			self._connection = sqlite3.connect(":memory:")  # type: Any
		else:
			self._connection = sqlite3.connect(self._setting['postgresql']['connect'])  # fixme ファイル指定
		logger.debug("sqlite3接続 :%s", pformat(self._connection))
		self._dbms = 'sqlite'

	def execute(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> None:
		if param is None:
			cursor = self._connection.execute(sql)
		else:
			cursor = self._connection.execute(sql, param)
		logger.debug("rowcount :%s", cursor.rowcount)

	def execute_fetchall(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> List[Dict[str, Any]]:
		self._connection.row_factory = sqlite3.Row
		if param is None:
			cursor = self._connection.execute(sql)
		else:
			cursor = self._connection.execute(sql, param)
		logger.debug("rowcount :%s", cursor.rowcount)

		ret_list = []
		for row in cursor:
			item = {}
			for k in row.keys():
				item[k] = row[k]
			ret_list.append(item)

		return ret_list

	def execute_fetchall_namedtuple(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None, *, namedtuple=None, tuplename: str = 'namedtuple'):
		pass  # TODO 実装する

	def close(self) -> None:
		logger.debug("接続クローズ :%s", pformat(self._connection))
		self._connection.close()

	def __enter__(self):
		logger.debug("with 開始")
		return self

	def __exit__(self, exception_type, exception_value, traceback) -> None:
		self.close()
		logger.debug("with 終了")


class Postgresql(Database):

	def _connect(self) -> None:
		logger.debug('Postgresqlインスタンス 初期化')
		self._dbms = 'postgresql'
		self._connection = psycopg2.connect(self._setting['postgresql']['connect'])
		logger.debug("Postgresql接続 :%s", pformat(self._connection))

	def execute(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> None:
		with self._connection.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql.replace('?', '%s'), param)

		logger.debug("sql :%s", sql)
		logger.debug("query :%s", cur.query.decode('utf-8'))

	def execute_fetchall(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None) -> List[Dict[str, Any]]:
		result = []
		with self._connection.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql, param)
			for row in cur:
				result.append(dict(row))

		logger.debug("description :%s", pformat(cur.description))
		logger.debug("sql :%s", sql)
		logger.debug("query :%s", cur.query.decode('utf-8'))

		return result

	def execute_fetchall_namedtuple(self, sql: str, param: Union[tuple, List[Union[str, int]]] = None, *, namedtuple=None, tuplename: str = 'namedtuple'):
		result = []
		with self._connection.cursor() as cur:
			cur.execute(sql, param)
			rows = cur.fetchall()
			if namedtuple is None:
				namedtuple = collections.namedtuple(tuplename, list(map(lambda x: x.name, cur.description)))

			for row in rows:
				result.append(namedtuple(*row))

		logger.debug("description :%s", pformat(cur.description))
		logger.debug("sql :%s", sql)
		logger.debug("query :%s", cur.query.decode('utf-8'))

		return result


def get_db(setting: ConfigParser = None) -> Database:
	# TODO SQLite ファイル対応
	if setting is None or psycopg2 is None:
		db = Database()
	else:
		db = Postgresql(setting)
	return db
