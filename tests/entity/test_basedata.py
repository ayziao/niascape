from unittest import TestCase

import niascape
from niascape.entity import basedata
from niascape.utility.database import get_db

import logging
from pprint import pformat

logger = logging.getLogger(__name__)


# logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


class TestBasedata(TestCase):
	_db = None

	@classmethod
	def setUpClass(cls):
		db = get_db(niascape._read_ini('config.ini.sample')['database'])
		logger.debug(db.dbms)
		# db = get_db(niascape.ini)
		# db = get_db()

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

	def test_daycount(self):
		db = self._db

		ref = basedata._daycount(db)
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
		self.assertEqual('2018-01-01', ref[0].date)
		# self.assertEqual('2018-02-18', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = basedata._daycount(db, 'test', '#tag')
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		self.assertEqual('2018-01-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = basedata._daycount(db, 'test', '#tag', 'body')
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		self.assertEqual('2018-01-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = basedata._daycount(db, 'test', search_body='body')
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		self.assertEqual('2018-01-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		#
		# ref = basedata._daycount(db, 'test', '#test', 'test')
		# logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		# # self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
		# self.assertEqual('2016-12-30', ref[0].date)
		# self.assertEqual(1, ref[0].count)
		#
		# ref = basedata._daycount(db, 'test', search_body='test')
		# logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		# # self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
		# self.assertEqual('2017-04-18', ref[0].date)
		# self.assertEqual(1, ref[0].count)
		pass

	def test_tag_count(self):
		db = self._db
		ref = basedata._tag_count(db)

		logger.debug("タグ件数\n%s", pformat(ref[:3]))
		self.assertEqual({'count': 3, 'tag': '#tag'}, ref[0])

		# self.assertEqual({'count': 353, 'tag': 'twitter_posted'}, ref[0])
		pass

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
		# self.assertEqual('20180218232339289972', ref[0].identifier)
		pass
