from unittest import TestCase

from typing import NamedTuple

try:
	import psycopg2
except ImportError:
	pass

from niascape.utility.database import Database
import niascape

import logging

logger = logging.getLogger(__name__)


# logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


class TestDatabase(TestCase):
	_db = None

	@classmethod
	def setUpClass(cls):
		ini = niascape._read_ini('config.ini.sample')  # TODO configパーサーオブジェクトやめる
		niascape.ini = ini
		cls._db = Database(ini)
		ret = cls._db.execute_fetchall("select version()")
		logger.debug(ret)
		ret = cls._db.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
		logger.debug(ret)
		ret = TestDatabase._db.execute("INSERT INTO test(num,data) VALUES (%s,%s)", (1, "hoge"))
		logger.debug(ret)

	@classmethod
	def tearDownClass(cls):
		cls._db.close()

	def test_hoge(self):
		ret = TestDatabase._db.execute("INSERT INTO test(num,data) VALUES (%s,%s)", (1, "hoge"))
		logger.debug(ret)
		ret = TestDatabase._db.execute_fetchall("select * from test")
		logger.debug(ret)

	def test_init_ps(self):
		ini = niascape._read_ini('config.ini.sample')  # TODO configパーサーオブジェクトやめる
		niascape.ini = ini
		with Database(ini) as db:
			self.assertEqual(Database, type(db))
			self.assertEqual('postgresql', db._dbms)

	def test_init_sqlite(self):
		with Database() as db:
			self.assertEqual(Database, type(db))
			self.assertEqual('sqlite', db._dbms)

	def test__get_connection_ps(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini
		con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
		with Database(ini) as db:
			ret = db._get_connection_ps(con)
			self.assertEqual(psycopg2.extensions.connection, type(ret))

	def test__get_connection_sqlite(self):
		self.skipTest('未実装')  # TODO 実装

	def test_execute(self):
		with Database() as db:
			db.execute("CREATE TABLE dummy (num int(10) NOT NULL,str varchar(500) NOT NULL, PRIMARY KEY(num))")
			db.execute("INSERT INTO dummy VALUES(1, '1')")
			db.execute("INSERT INTO dummy VALUES(?, ?)", (2, '2'))
			db.execute("INSERT INTO dummy VALUES(?, ?)", (3, '3'))
			ret = db.execute_fetchall("SELECT * FROM dummy")
			logger.debug('select all %s', ret)
			self.assertEqual({'num': 1, 'str': '1'}, ret[0])
			ret = db.execute_fetchall("SELECT * FROM dummy WHERE num = ?", (2,))
			self.assertEqual({'num': 2, 'str': '2'}, ret[0])
			logger.debug('select one %s', ret)

	def test_execute_fetchall(self):
		ret = TestDatabase._db.execute_fetchall("select * from test")
		logger.debug(ret)
		self.assertEqual(1, ret[0]['id'])

	def test_execute_fetchall_namedtuple(self):
		ret = TestDatabase._db.execute_fetchall_namedtuple("select * from test")
		logger.debug(ret)
		self.assertEqual(1, ret[0].id)

	def test_execute_fetchall_namedtuple_set(self):
		count = NamedTuple('count', (('name', str), ('count', int)))
		ret = TestDatabase._db.execute_fetchall_namedtuple("select 'hoge' as name , COUNT(*) as count from test", namedtuple=count)
		logger.debug(ret)
		self.assertEqual(1, ret[0].count)
