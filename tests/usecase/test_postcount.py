from unittest import TestCase, mock, skip

import niascape
from niascape import usecase
from niascape.repository import postcount
from niascape.utility.database import Database


class TestPostcount(TestCase):
	@classmethod
	def setUpClass(cls):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini

	def test_top(self):
		ret = usecase.top({})
		self.assertEqual('top', ret)

	@mock.patch('niascape.usecase.postcount.postcount')
	def test_day(self, moc):
		self.assertTrue(hasattr(postcount, 'day'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site='', tag='', search_body=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock daycount {site} {tag} {search_body}".strip()

		moc.day = method

		ref = usecase.postcount.day({})
		self.assertEqual('called mock daycount', ref)

		ref = usecase.postcount.day({'site': 'test', 'tag': '#test', 'search_body': 'test'})
		self.assertEqual('called mock daycount test #test test', ref)

	@mock.patch('niascape.usecase.postcount.postcount')
	def test_month(self, moc):
		self.assertTrue(hasattr(postcount, 'month'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site='', tag='', search_body=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock monthcount {site} {tag} {search_body}".strip()

		moc.month = method

		ref = usecase.postcount.month({})
		self.assertEqual('called mock monthcount', ref)

		ref = usecase.postcount.month({'site': 'test', 'tag': '#test', 'search_body': 'test'})
		self.assertEqual('called mock monthcount test #test test', ref)

	@mock.patch('niascape.usecase.postcount.postcount')
	def test_hour(self, moc):
		self.assertTrue(hasattr(postcount, 'hour'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site='', tag='', search_body=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock hourcount {site} {tag} {search_body}".strip()

		moc.hour = method

		ref = usecase.postcount.hour({})
		self.assertEqual('called mock hourcount', ref)

	@mock.patch('niascape.usecase.postcount.postcount')
	def test_week(self, moc):
		self.assertTrue(hasattr(postcount, 'week'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site='', tag='', search_body=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock weekcount {site} {tag} {search_body}".strip()

		moc.week = method

		ref = usecase.postcount.week({})
		self.assertEqual('called mock weekcount', ref)

	@skip("モックなし確認用")
	def test_day_no_mock(self):
		ini = niascape._read_ini('config.ini')
		niascape.ini = ini
		ref = usecase.postcount.day({'site': 'test', 'tag': '#test'})
		self.assertEqual('[{"date": "2016-12-30", "count": 1}, {"date": "2016-10-26", "count": 1}, {"date": "2015-07-10", "count": 1}]', ref)

	@mock.patch('niascape.usecase.postcount.postcount')
	def test_tag_count(self, moc):
		self.assertTrue(hasattr(postcount, 'tag'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock _tag_count {site}".strip()

		moc.tag = method

		ref = usecase.postcount.tag({})
		self.assertEqual('called mock _tag_count', ref)

		ref = usecase.postcount.tag({'site': 'test'})
		self.assertEqual('called mock _tag_count test', ref)
