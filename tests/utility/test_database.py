from unittest import TestCase, skipUnless

from typing import NamedTuple

try:
	import psycopg2
except ImportError:
	psycopg2 = None

from niascape.utility.database import Database, Postgresql, get_db
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
		db = get_db(ini['database_sqlite'])
		ret = db.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
		logger.debug(ret)
		ret = db.execute("INSERT INTO test(id, num, data) VALUES (?, ?, ?)", (1, 1, "hoge"))
		ret = db.execute("INSERT INTO test(id, num, data) VALUES (?, ?, ?)", (2, 2, "piyp"))
		ret = db.execute("INSERT INTO test(id, num, data) VALUES (?, ?, ?)", (3, 3, "fuga"))
		ret = db.execute("INSERT INTO test(id, num, data) VALUES (?, ?, ?)", (4, 4, "ham"))
		logger.debug(ret)
		cls._db = db

	@classmethod
	def tearDownClass(cls):
		cls._db.close()

	def test_instance(self):
		self.assertEqual(Database, type(self._db))
		self.assertIsInstance(self._db, Database)
		self.assertEqual('sqlite', self._db.dbms)

		db = get_db()
		self.assertIsInstance(db, Database)
		self.assertEqual('sqlite', db.dbms)

	def test_execute(self):
		db = self._db

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

	def test_fetchall(self):
		db = self._db

		ret = db.execute_fetchall("SELECT * FROM test")
		self.assertEqual({'data': 'hoge', 'id': 1, 'num': 1}, ret[0])

	def test_fetc_page(self):
		db = self._db

		ret = db.execute_fetch_page("SELECT * FROM test")
		self.assertEqual({'data': 'hoge', 'id': 1, 'num': 1}, ret[0])

		ret = db.execute_fetch_page("SELECT * FROM test", page="aaa")
		self.assertEqual({'data': 'hoge', 'id': 1, 'num': 1}, ret[0])

		ret = db.execute_fetch_page("SELECT * FROM test", page=2, per_page=2)
		self.assertEqual({'data': 'fuga', 'id': 3, 'num': 3}, ret[0])

	def test_execute_fetchall_namedtuple(self):
		db = self._db

		ret = db.execute_fetchall("SELECT * FROM test WHERE id = ?", (1,), tuple_name='test')
		self.assertEqual(1, ret[0].id)
		self.assertEqual(1, ret[0].num)
		self.assertEqual('hoge', ret[0].data)

		count = NamedTuple('count', (('name', str), ('count', int)))
		ret = self._db.execute_fetchall("select 'hoge' as name , COUNT(*) as count from test", namedtuple=count)
		self.assertEqual(4, ret[0].count)


@skipUnless(psycopg2, 'psycopg2無し')
class TestPostgresql(TestCase):
	_db = None

	@classmethod
	def setUpClass(cls):
		ini = niascape._read_ini('config.ini.sample')  # TODO configパーサーオブジェクトやめる
		niascape.ini = ini
		cls._db = get_db(ini['database'])
		ret = cls._db.execute_fetchall("select version()")
		logger.debug(ret)
		ret = cls._db.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
		logger.debug(ret)
		ret = cls._db.execute("INSERT INTO test(num,data) VALUES (%s,%s)", (1, "hoge"))
		ret = cls._db.execute("INSERT INTO test(num,data) VALUES (%s,%s)", (2, "piyp"))
		ret = cls._db.execute("INSERT INTO test(num,data) VALUES (%s,%s)", (3, "fuga"))
		ret = cls._db.execute("INSERT INTO test(num,data) VALUES (%s,%s)", (4, "ham"))
		logger.debug(ret)

	@classmethod
	def tearDownClass(cls):
		cls._db.close()

	def test_instance(self):
		self.assertEqual(Postgresql, type(self._db))
		self.assertIsInstance(self._db, Database)
		self.assertIsInstance(self._db, Postgresql)
		self.assertEqual('postgresql', self._db.dbms)
		self.assertEqual(psycopg2.extensions.connection, type(self._db._connection))

	def test_execute(self):
		db = self._db
		db.execute('CREATE TABLE dummy ("num" int NOT NULL,"str" varchar(500) NOT NULL, PRIMARY KEY("num"))')
		ret = db.execute("INSERT INTO dummy VALUES(1, '1')")
		ret = db.execute("INSERT INTO dummy VALUES(%s, %s)", (2, '2'))
		ret = db.execute("INSERT INTO dummy VALUES(?, ?)", (3, "');DROP TABLE dummy;"))
		logger.debug(ret)
		ret = db.execute_fetchall("select * from dummy")
		logger.debug(ret)
		ret = self._db.execute_fetchall("select COUNT(*) as count from dummy", tuple_name='count')
		self.assertEqual(3, ret[0].count)

	def test_execute_fetchall(self):
		ret = self._db.execute_fetchall("select * from test")
		logger.debug(ret)
		self.assertEqual(1, ret[0]['id'])

	def test_execute_fetchall_namedtuple(self):
		ret = self._db.execute_fetchall_namedtuple("select * from test")
		logger.debug(ret)
		self.assertEqual(1, ret[0].id)

	def test_execute_fetchall_namedtuple_set(self):
		count = NamedTuple('count', (('name', str), ('count', int)))
		ret = self._db.execute_fetchall("select 'hoge' as name , COUNT(*) as count from test", namedtuple=count)
		logger.debug(ret)
		self.assertEqual(4, ret[0].count)
