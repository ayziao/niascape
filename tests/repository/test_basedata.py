from unittest import TestCase

import logging.config
from pprint import pformat

# import json ; logging.addLevelName(5, 'TRACE') ; logging.config.dictConfig(json.load(open('../logger_config.json', 'r')))

logger = logging.getLogger(__name__)

import niascape
from niascape.repository import basedata
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

	def test_get(self):
		db = self._db
		ref = basedata.get(db, '20170101235959999000', 'test')
		self.assertEqual('20170101235959999000', ref.identifier)

		ref = basedata.get(db, '20170101235959999001', 'test')
		self.assertEqual(None, ref)


	def test_timeline(self):
		db = self._db

		ref = basedata.timeline(db)
		logger.debug("basedata\n%s", pformat(ref[:5]))
		self.assertEqual('20170101235959999000', ref[0].identifier)

		ref = basedata.timeline(db, 'test', 2)
		logger.debug("basedata\n%s", pformat(ref[:5]))
		self.assertEqual([], ref)

		ref = basedata.timeline(db, 'dummy')
		logger.debug("basedata\n%s", pformat(ref[:5]))
		self.assertEqual('20180101123456789000', ref[0].identifier)

		# FUTURE やっつけ エンティティのテスト書いたら移動
		dic = ref[0]._asdict()
		self.assertEqual('20180101123456789000', dic["identifier"])

	def test_tagtimeline(self):
		db = self._db

		ref = basedata.tagtimeline(db, site='test', tag='tag')
		self.assertEqual('20170101235959999000', ref[0].identifier)

		ref = basedata.tagtimeline(db, site='test', tag='tag', order='ASC')
		self.assertEqual('20170101235959999000', ref[2].identifier)

	def test_search_body(self):
		db = self._db

		ref = basedata.search_body(db, site='test', searchbody='body')
		self.assertEqual('12345678901234567890', ref[0].identifier)

		ref = basedata.search_body(db, site='test', searchbody='hoge', order='ASC')
		self.assertEqual('20170101000000000000', ref[0].identifier)

	def test_day_timeline(self):
		db = self._db

		ref = basedata.day_timeline(db, site='test', date='2017')
		self.assertEqual('20170101000000000000', ref[0].identifier)
		self.assertEqual('20170101235959999000', ref[1].identifier)

		ref = basedata.day_timeline(db, site='test', date='2017', order='DESC')
		self.assertEqual('20170101235959999000', ref[0].identifier)

	def test_next_identifier(self):
		db = self._db
		ref = basedata.next_identifier(db, site='test', date='20160101')
		self.assertEqual('20170101000000000000', ref)

		ref = basedata.next_identifier(db, site='test', date='99999999')
		self.assertEqual('', ref)

	def test_prev_identifier(self):
		db = self._db
		ref = basedata.prev_identifier(db, site='test', date='20160101')
		self.assertEqual('19700101123456789000', ref)

		ref = basedata.prev_identifier(db, site='test', date='00000000')
		self.assertEqual('', ref)
