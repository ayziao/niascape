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


# PENDING DBMS別にクラス作る？ 継承？

class Database:
	@classmethod
	def get_instance(cls, setting):
		return Database(setting)

	def __init__(self, setting=None):
		logger.debug('Databaseインスタンス 初期化')
		self._setting = setting
		self._connection = None
		self._dbms = ''
		self._connect()

	def _connect(self):
		# TODO SQLite ファイル対応
		if self._setting is None or psycopg2 is None:
			self._dbms = 'sqlite'
			self._connection = self._get_connection_sqlite()
		else:
			self._dbms = 'postgresql'
			self._connection = self._get_connection_ps(self._setting['postgresql']['connect'])

	def _get_connection_ps(self, con):
		connection = psycopg2.connect(con)
		logger.debug("ポストグレス接続 :%s", pformat(connection))

		return connection

	def _get_connection_sqlite(self, con=None):
		if con is None:
			connection = sqlite3.connect(":memory:")
		else:
			connection = sqlite3.connect(con)  # fixme ファイル指定
		logger.debug("sqlite3接続 :%s", pformat(connection))
		return connection

	def execute(self, sql, param=None):
		if self._dbms == 'postgresql':
			with self._connection.cursor(cursor_factory=DictCursor) as cur:
				cur.execute(sql, param)

			logger.debug("sql :%s", sql)
			logger.debug("query :%s", cur.query.decode('utf-8'))
		else:
			if param is None:
				cursor = self._connection.execute(sql)
			else:
				cursor = self._connection.execute(sql, param)
			logger.debug("rowcount :%s", cursor.rowcount)

	def execute_fetchall(self, sql, param=None):
		if self._dbms == 'postgresql':
			result = []
			with self._connection.cursor(cursor_factory=DictCursor) as cur:
				cur.execute(sql, param)
				for row in cur:
					result.append(dict(row))

			logger.debug("description :%s", pformat(cur.description))
			logger.debug("sql :%s", sql)
			logger.debug("query :%s", cur.query.decode('utf-8'))

			return result
		else:
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

	def execute_fetchall_namedtuple(self, sql, param=None, *, namedtuple=None, tuplename='namedtuple'):
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

	def close(self):
		logger.debug("接続クローズ :%s", pformat(self._connection))
		self._connection.close()

	def __enter__(self):
		logger.debug("with 開始")
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.close()
		logger.debug("with 終了")


class Setting:
	def __init__(self):
		self.ini = None

	def _load_setting(self):
		pass

	def get_setting(self):
		pass

