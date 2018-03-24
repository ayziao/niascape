import collections

import psycopg2
from psycopg2.extras import DictCursor

import logging
from pprint import pformat

logger = logging.getLogger(__name__)


class Database:
	@classmethod
	def get_instance(cls, setting):
		return Database(setting)

	def __init__(self, setting):
		logger.debug('Databaseインスタンス 初期化')
		self._setting = setting
		self._conection = None
		self._connect()

	def _connect(self):
		# TODO SQLite対応
		self._conection = self._get_conection_ps(self._setting['postgresql'].get('connect'))

	def _get_conection_ps(self, con):
		conection = psycopg2.connect(con)
		logger.debug("ポストグレス接続 :%s", pformat(self._conection))

		return conection

	def _get_conection_sqlite(self):
		pass

	def execute(self, sql, *, param=None):
		pass

	def execute_fetchall(self, sql, *, param=None):
		result = []
		with self._conection.cursor(cursor_factory=DictCursor) as cur:
			cur.execute(sql, param)
			for row in cur:
				result.append(dict(row))

		logger.debug("description :%s", pformat(cur.description))
		logger.debug("sql :%s", sql)
		logger.debug("query :%s", cur.query.decode('utf-8'))

		return result

	def execute_fetchall_namedtuple(self, sql, param=None, *, namedtuple=None, tuplename='namedtuple'):
		result = []
		with self._conection.cursor() as cur:
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
		logger.debug("接続クローズ :%s", pformat(self._conection))
		self._conection.close()

	def __enter__(self):
		logger.debug("with 開始")
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.close()
		logger.debug("with 終了")
