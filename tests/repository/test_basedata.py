from unittest import TestCase

import logging.config
from pprint import pformat

# import json ; logging.config.dictConfig(json.load(open('../logger_config.json', 'r')))

logger = logging.getLogger(__name__)

import niascape
from niascape.repository import basedata
from niascape.repository import site
from niascape.utility.database import get_db


class TestBasedata(TestCase):
	_db = None

	@classmethod
	def setUpClass(cls):
		db = get_db(niascape._read_ini('config.ini.sample')['database'])
		# db = get_db()
		logger.debug(db.dbms)

		create_sql = """
		CREATE TABLE "basedata" (
			"site"	varchar(63),
			"identifier"	varchar(20),
			"datetime"	timestamp NOT NULL,
			"title"	TEXT NOT NULL DEFAULT '',
			"tags"	TEXT NOT NULL DEFAULT '',
			"body"	TEXT NOT NULL DEFAULT '',
			PRIMARY KEY("site","identifier")
		);
		"""
		ret = db.execute(create_sql)
		logger.debug(ret)
		insert_sql = 'INSERT INTO "basedata" VALUES(?, ?, ?, ?, ?, ?);'

		ret = db.execute(insert_sql, ('test', '12345678901234567890', '2018-01-01 00:00:00.000', 'title', ' #tag ', 'body'))
		ret = db.execute(insert_sql, ('test', '19700101123456789000', '1970-01-01 12:34:56.789', '19700101123456789000', '', 'test'))
		ret = db.execute(insert_sql, ('test', '20170101235959999000', '2017-01-01 23:59:59.999', '20170101235959999000', ' #tag system:1234 ', 'hoge'))
		ret = db.execute(insert_sql, ('test', '20170101000000000000', '2017-01-01 00:00:00.000', '20170101000000000000', ' #tag system:1234 ', 'hoge2'))
		ret = db.execute(insert_sql, ('dummy', '20180101123456789000', '2018-01-01 12:34:56.789', 'dummy', '', 'dummy'))
		logger.debug(ret)
		cls._db = db

	@classmethod
	def tearDownClass(cls):
		cls._db.close()

	def test_get_all(self):
		db = self._db

		ref = basedata.get_all(db)
		logger.debug("basedata\n%s", pformat(ref[:5]))
		self.assertEqual('20170101235959999000', ref[0].identifier)

		ref = basedata.get_all(db, 'test', 2)
		logger.debug("basedata\n%s", pformat(ref[:5]))
		self.assertEqual([], ref)

		ref = basedata.get_all(db, 'dummy')
		logger.debug("basedata\n%s", pformat(ref[:5]))
		self.assertEqual('20180101123456789000', ref[0].identifier)

		# FIXME やっつけ エンティティのテスト書いたら移動
		dic = ref[0]._asdict()
		self.assertEqual('20180101123456789000', dic["identifier"])


	# print(ref[0].__dict__)

	def test_site_list(self): #FIXME ベースデータにサイトアレしてるのでやっつけ サイトテーブル作ったら移動
		db = self._db

		ref = site.sites(db)
		self.assertEqual([{'site': 'test', 'count': 4}, {'site': 'dummy', 'count': 1}], ref)
