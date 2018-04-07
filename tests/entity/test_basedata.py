import unittest

import niascape
from niascape.entity import basedata
from niascape.utility.database import Database

import logging
from pprint import pformat

logger = logging.getLogger(__name__)


# logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


@unittest.skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
class TestBasedata(unittest.TestCase):

	def test_daycount(self):
		ini = niascape._read_ini('config.ini.sample')
		# niascape.ini = ini
		with Database.get_instance(ini) as conn:
			ref = basedata._daycount(conn)
			logger.debug("日別投稿数\n%s", pformat(ref[:3]))
			# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
			self.assertEqual('2018-02-18', ref[0].date)
			self.assertEqual(2, ref[0].count)

			ref = basedata._daycount(conn, 'test', '#test', 'test')
			logger.debug("日別投稿数\n%s", pformat(ref[:3]))
			# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
			self.assertEqual('2016-12-30', ref[0].date)
			self.assertEqual(1, ref[0].count)

			ref = basedata._daycount(conn, 'test', search_body='test')
			logger.debug("日別投稿数\n%s", pformat(ref[:3]))
			# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
			self.assertEqual('2017-04-18', ref[0].date)
			self.assertEqual(1, ref[0].count)

	def test_tag_count(self):
		ini = niascape._read_ini('config.ini.sample')
		# niascape.ini = ini
		with Database.get_instance(ini) as db:
			ref = basedata._tag_count(db)

		logger.debug("タグ件数\n%s", pformat(ref[:3]))
		self.assertEqual({'count': 353, 'tag': 'twitter_posted'}, ref[0])

	def test_get_all(self):
		ini = niascape._read_ini('config.ini.sample')
		# niascape.ini = ini
		with Database.get_instance(ini) as db:
			ref = basedata.get_all(db)

		logger.debug("basedata\n%s", pformat(ref[:3]))
		self.assertEqual('20180218232339289972', ref[0].identifier)
