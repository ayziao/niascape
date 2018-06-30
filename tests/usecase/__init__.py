from unittest import TestCase, mock

import niascape
from niascape import usecase
from niascape.repository import basedata
from niascape.utility.database import Database


class TestUsecase(TestCase):
	@classmethod
	def setUpClass(cls):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini

	def test_top(self):
		ret = usecase.top({})
		self.assertEqual('top', ret)

	@mock.patch('niascape.usecase.basedata')
	def test_getdata(self, moc):
		self.assertTrue(hasattr(basedata, 'get'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, identifier, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock get {identifier} {site}".strip()

		moc.get = method

		ref = usecase.getdata({'identifier': '', 'site': ''})
		self.assertEqual('called mock get', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_timeline(self, moc):
		self.assertTrue(hasattr(basedata, 'timeline'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock timeline {site}".strip()

		moc.timeline = method

		ref = usecase.timeline({})
		self.assertEqual('called mock timeline', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_tagtimeline(self, moc):
		self.assertTrue(hasattr(basedata, 'tagtimeline'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock tagtimeline {site}".strip()

		moc.tagtimeline = method

		ref = usecase.tagtimeline({})
		self.assertEqual('called mock tagtimeline', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_search_body(self, moc):
		self.assertTrue(hasattr(basedata, 'search_body'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock search_body {site}".strip()

		moc.search_body = method

		ref = usecase.searchbody({})
		self.assertEqual('called mock search_body', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_day_summary(self, moc):
		self.assertTrue(hasattr(basedata, 'day_timeline'))  # モックだと関数名の修正についていけないのでチェック
		self.assertTrue(hasattr(basedata, 'next_identifier'))  # モックだと関数名の修正についていけないのでチェック
		self.assertTrue(hasattr(basedata, 'prev_identifier'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site='', date=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [f"called mock day_timeline {site}".strip()]

		def method2(conn, site='', date=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock {site} {date}".strip()

		moc.day_timeline = method
		moc.next_identifier = method2
		moc.prev_identifier = method2

		ref = usecase.day_summary({'site': 'test', 'date': '19990701'})
		self.assertEqual({"content": ["called mock day_timeline test"], "next": "called m", "prev": "called m"}, ref)
