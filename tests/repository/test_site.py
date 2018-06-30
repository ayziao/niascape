from unittest import TestCase

import json
import logging.config

# logging.addLevelName(5, 'TRACE') ; logging.config.dictConfig(json.load(open('../logger_config.json', 'r')))

logger = logging.getLogger(__name__)

import niascape
from niascape.repository import site
from niascape.utility.database import get_db


class TestSite(TestCase):
	_db = None

	@classmethod
	def setUpClass(cls):
		db = get_db(niascape._read_ini('config.ini.sample')['database'])

		logger.debug(db.dbms)

		# FUTURE ベースデータにサイトアレしてるのでやっつけ サイトテーブル作る
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

		create_sql = """
		CREATE TABLE "keyvalue" (
			"key" TEXT NOT NULL,
			"value" TEXT NOT NULL DEFAULT '',
			PRIMARY KEY("key")
		);
		"""
		ret = db.execute(create_sql)
		logger.debug(ret)
		insert_sql = 'INSERT INTO "keyvalue" VALUES(?, ?);'

		ret = db.execute(insert_sql, ('key', 'val'))
		ret = db.execute(insert_sql, ('sitesetting_test', json.dumps({"siteinsert": "Insert text"})))

		cls._db = db

	@classmethod
	def tearDownClass(cls):
		cls._db.close()

	def test_site_list(self):  # FUTURE ベースデータにサイトアレしてるのでやっつけ サイトテーブル作る
		db = self._db

		ref = site.sites(db)
		self.assertEqual([{'site': 'test', 'count': 4}, {'site': 'dummy', 'count': 1}], ref)

	def test_site_setting(self):
		db = self._db

		ref = site.setting(db, 'test')
		self.assertEqual('Insert text', ref['siteinsert'])
