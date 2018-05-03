from unittest import TestCase

import logging.config
from pprint import pformat

# import json ; logging.config.dictConfig(json.load(open('../logger_config.json', 'r')))

logger = logging.getLogger(__name__)

import niascape
from niascape.repository import postcount
from niascape.utility.database import get_db


class TestPostcount(TestCase):
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

		ref = postcount.day(db)
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
		self.assertEqual('2018-01-01', ref[0].date)
		# self.assertEqual('2018-02-18', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = postcount.day(db, 'test', tag='#tag')
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		self.assertEqual('2018-01-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = postcount.day(db, 'test', '#tag', 'body')
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		self.assertEqual('2018-01-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = postcount.day(db, 'test', search_body='body')
		logger.debug("日別投稿数\n%s", pformat(ref[:3]))
		self.assertEqual('2018-01-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = postcount.day(db, **{'site': 'test', 'tag': '#tag', 'search_body': 'body'})
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

	def test_monthcount(self):
		db = self._db
		ref = postcount.month(db)
		self.assertEqual('1970-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = postcount.month(db, 'dummy')
		self.assertEqual('2018-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = postcount.month(db, 'test', tag='#tag')
		self.assertEqual('2017-01', ref[0].date)
		self.assertEqual(2, ref[0].count)

		ref = postcount.month(db, 'test', search_body='body')
		self.assertEqual('2018-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

		ref = postcount.month(db, **{'site': 'test', 'tag': '#tag', 'search_body': 'body'})
		self.assertEqual('2018-01', ref[0].date)
		self.assertEqual(1, ref[0].count)

	def test_tag_count(self):
		db = self._db
		ref = postcount.tag(db)

		logger.debug("タグ件数\n%s", pformat(ref[:3]))
		self.assertEqual({'count': 3, 'tag': '#tag'}, ref[0])

		# self.assertEqual({'count': 353, 'tag': 'twitter_posted'}, ref[0])
		pass
