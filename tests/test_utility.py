from unittest import TestCase, skip

import json
import collections
from typing import NamedTuple

try:
	import psycopg2
except ImportError:
	pass

from niascape.utility import Database, AsdictSupportJSONEncoder
import niascape

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


class TestDatabase(TestCase):
	_db = None

	@classmethod
	def setUpClass(cls):
		print("setup")
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

	# @skip("postgresqlのテストを保留")  # TODO データベースに接続してのテストについて考える
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

	# @skip("postgresqlのテストを保留")  # TODO データベースに接続してのテストについて考える
	def test__get_connection_ps(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini
		con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる

		db = Database(ini)
		ret = db._get_connection_ps(con)
		# pprint(ret)
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

	# @skip("postgresqlのテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_execute_fetchall(self):
		ret = TestDatabase._db.execute_fetchall("select * from test")
		logger.debug(ret)
		self.assertEqual(1, ret[0]['id'])

	#
	# ini = niascape._read_ini('config.ini.sample')
	# niascape.ini = ini
	#
	# with Database(ini) as db:
	# 	sql = """
	# 	SELECT * FROM basedata
	# 	WHERE
	# 		site = 'test'
	# 	ORDER BY "datetime" DESC
	# 	LIMIT 1
	# 	"""
	# 	ret = db.execute_fetchall(sql)
	# 	# pprint(ret)
	# 	self.assertEqual('20180218232339289972', ret[0]['identifier'])

	# @skip("postgresqlのテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_execute_fetchall_namedtuple(self):
		ret = TestDatabase._db.execute_fetchall_namedtuple("select * from test")
		logger.debug(ret)
		self.assertEqual(1, ret[0].id)

	#
	# ini = niascape._read_ini('config.ini.sample')
	# # db = Database(ini)
	#
	# with Database.get_instance(ini) as db:
	# 	logger.debug('Databaseインスタンス 初期化')
	# 	sql = """
	# 	SELECT * FROM basedata
	# 	WHERE
	# 		site = 'test'
	# 	ORDER BY "datetime" DESC
	# 	LIMIT 1
	# 	"""
	# 	ret = db.execute_fetchall_namedtuple(sql, tuplename='basedata')
	# 	# pprint(ret)
	# 	self.assertEqual('20180218232339289972', ret[0].identifier)

	# @skip("postgresqlのテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_execute_fetchall_namedtuple_set(self):
		count = NamedTuple('count', (('name', str), ('count', int)))
		ret = TestDatabase._db.execute_fetchall_namedtuple("select 'hoge' as name , COUNT(*) as count from test", namedtuple=count)
		logger.debug(ret)
		self.assertEqual(1, ret[0].count)

	#
	# ini = niascape._read_ini('config.ini.sample')
	# # db = Database(ini)
	# with Database(ini) as db:
	# 	sql = """
	# 	SELECT
	# 		regexp_replace(tags , ':[0-9]+','') as "tags",
	# 		COUNT(*) as "count"
	# 	FROM basedata
	# 	WHERE
	# 		site = %s
	# 	GROUP BY regexp_replace(tags , ':[0-9]+','')
	# 	ORDER BY COUNT(*) DESC
	# 	LIMIT %s
	# 	"""
	# 	tagcount = NamedTuple('tagcount', (('tags', str), ('count', int)))
	# 	ret = db.execute_fetchall_namedtuple(sql, ('test', 3), namedtuple=tagcount)
	# 	# pprint(ret)
	# 	self.assertEqual(' twitter_posted ', ret[0].tags)


class TestAsdictSupportJSONEncoder(TestCase):
	def test_encode(self):
		ret = json.dumps(None, cls=AsdictSupportJSONEncoder)
		self.assertEqual('null', ret)
		ret = json.dumps(True, cls=AsdictSupportJSONEncoder)
		self.assertEqual('true', ret)
		ret = json.dumps(False, cls=AsdictSupportJSONEncoder)
		self.assertEqual('false', ret)
		ret = json.dumps(1, cls=AsdictSupportJSONEncoder)
		self.assertEqual('1', ret)
		ret = json.dumps(1.1, cls=AsdictSupportJSONEncoder)
		self.assertEqual('1.1', ret)
		ret = json.dumps('hoge', cls=AsdictSupportJSONEncoder)
		self.assertEqual('"hoge"', ret)

	def test_encode_list(self):
		test = list()
		test.append('hoge')
		test.append(1)
		test.append(1.1)
		test.append([])
		test.append({})
		test.append(True)
		test.append(False)
		test.append(None)

		ret = json.dumps(test, cls=AsdictSupportJSONEncoder)
		self.assertEqual('["hoge", 1, 1.1, [], {}, true, false, null]', ret)

	def test_encode_dict(self):
		_dict = dict()
		_dict["str"] = 'hoge'
		_dict["int"] = 1
		_dict["float"] = 1.1
		_dict["list"] = []
		_dict["dict"] = {}
		_dict["true"] = True
		_dict["false"] = False
		_dict["none"] = None
		_dict[True] = "True"
		_dict[False] = "False"
		_dict[None] = "None"

		ret = json.dumps(_dict, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"str": "hoge", "int": 1, "float": 1.1, "list": [], "dict": {}, "true": true, "false": false, "none": null, "true": "True", "false": "False", "null": "None"}', ret)

	def test_encode_tuple(self):
		_tuple = ('hoge', 1)
		ret = json.dumps(_tuple, cls=AsdictSupportJSONEncoder)
		self.assertEqual('["hoge", 1]', ret)

		namedtuple = NamedTuple('namedtuple', (('key', str), ('val', int)))
		_namedtuple = namedtuple(*_tuple)
		ret = json.dumps(_namedtuple, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"key": "hoge", "val": 1}', ret)

		ret = json.dumps([_namedtuple], cls=AsdictSupportJSONEncoder)
		self.assertEqual('[{"key": "hoge", "val": 1}]', ret)

		namedtuple = collections.namedtuple('collections_namedtuple', ('key', 'val'))
		_namedtuple = namedtuple(*_tuple)
		ret = json.dumps(_namedtuple, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"key": "hoge", "val": 1}', ret)
		ret = json.dumps([_namedtuple], cls=AsdictSupportJSONEncoder)
		self.assertEqual('[{"key": "hoge", "val": 1}]', ret)
