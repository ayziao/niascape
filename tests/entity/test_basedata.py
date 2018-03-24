import unittest

import psycopg2

import logging
from pprint import pformat

logger = logging.getLogger(__name__)

import niascape
from niascape.entity import basedata


class TestBasedata(unittest.TestCase):

	@unittest.skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_daycount(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini
		con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
		with psycopg2.connect(con) as conn:
			ref = basedata._daycount(conn)
			logger.debug("日別投稿数\n%s", pformat(ref))
			# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
			self.assertEqual('2018-02-18', ref[0].date)
			self.assertEqual(2, ref[0].count)

			ref = basedata._daycount(conn, 'test', '#test', 'test')
			logger.debug("日別投稿数\n%s", pformat(ref))
			# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
			self.assertEqual('2016-12-30', ref[0].date)
			self.assertEqual(1, ref[0].count)

			ref = basedata._daycount(conn, 'test', search_body='test')
			logger.debug("日別投稿数\n%s", pformat(ref))
			# self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
			self.assertEqual('2017-04-18', ref[0].date)
			self.assertEqual(1, ref[0].count)

	@unittest.skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_tag_count(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini
		con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
		with psycopg2.connect(con) as conn:
			ref = basedata._tag_count(conn)

		logger.debug("タグ件数\n%s", pformat(ref))
		self.assertEqual({'count': 353, 'tag': 'twitter_posted'}, ref[0])

	@unittest.skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_get_all(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini
		con = niascape.ini['postgresql'].get('connect')  # TODO クラス化してインスタンス化時にDBコネクションを受けとる
		with psycopg2.connect(con) as conn:
			ref = basedata.get_all(conn)

		logger.debug("basedata\n%s", pformat(ref))
		self.assertEqual('20180218232339289972', ref[0].identifier)
