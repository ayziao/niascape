from unittest import TestCase, skip

from typing import NamedTuple
import psycopg2

from niascape.utility import Database
import niascape

import logging

logger = logging.getLogger(__name__)


# logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


@skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
class TestDatabase(TestCase):
	def test_init(self):
		ini = niascape._read_ini('config.ini.sample')  # TODO configパーサーオブジェクトやめる
		niascape.ini = ini
		db = Database(ini)
		self.assertEqual(Database, type(db))

	def test__get_conection_ps(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini
		con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる

		db = Database(ini)
		ret = db._get_conection_ps(con)
		# pprint(ret)
		self.assertEqual(psycopg2.extensions.connection, type(ret))

	def test__get_conection_sqlite(self):
		self.skipTest('未実装')  # TODO 実装

	def test_execute(self):
		self.skipTest('未実装')  # TODO 実装

	def test_execute_fetchall(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini

		db = Database(ini)

		sql = """
		SELECT * FROM basedata
		WHERE
			site = 'test'
		ORDER BY "datetime" DESC
		LIMIT 1
		"""
		ret = db.execute_fetchall(sql)
		# pprint(ret)
		self.assertEqual('20180218232339289972', ret[0]['identifier'])
		db.close()

	def test_execute_fetchall_namedtuple(self):
		ini = niascape._read_ini('config.ini.sample')
		# db = Database(ini)

		with Database.get_instance(ini) as db:
			logger.debug('Databaseインスタンス 初期化')
			sql = """
			SELECT * FROM basedata
			WHERE
				site = 'test'
			ORDER BY "datetime" DESC
			LIMIT 1
			"""
			ret = db.execute_fetchall_namedtuple(sql, tuplename='basedata')
			# pprint(ret)
			self.assertEqual('20180218232339289972', ret[0].identifier)

	def test_execute_fetchall_namedtuple_set(self):
		ini = niascape._read_ini('config.ini.sample')
		# db = Database(ini)
		with Database(ini) as db:
			sql = """
			SELECT
				regexp_replace(tags , ':[0-9]+','') as "tags",
				COUNT(*) as "count"
			FROM basedata
			WHERE
				site = %s
			GROUP BY regexp_replace(tags , ':[0-9]+','')
			ORDER BY COUNT(*) DESC
			LIMIT %s
			"""
			tagcount = NamedTuple('tagcount', (('tags', str), ('count', int)))
			ret = db.execute_fetchall_namedtuple(sql, ('test', 3), namedtuple=tagcount)
			# pprint(ret)
			self.assertEqual(' twitter_posted ', ret[0].tags)
