from unittest import TestCase, mock, skip

import niascape
from niascape import action
from niascape.entity import basedata
from niascape.utility.database import Database


class Dummy:
	def __init__(self, dummy):
		self.dummy = dummy

	def _asdict(self):
		return {'dummy': self.dummy}


class TestAction(TestCase):
	@classmethod
	def setUpClass(cls):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini

	def test_top(self):
		ret = action.top({})
		self.assertEqual('top', ret)

	@mock.patch('niascape.action.basedata')
	def test_daycount(self, moc):
		self.assertTrue(hasattr(basedata, '_daycount'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site='', tag='', search_body=''):  # PENDING 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock daycount {site} {tag} {search_body}".strip())]

		moc._daycount = method

		ref = action.daycount({})
		self.assertEqual('[{"dummy": "called mock daycount"}]', ref)

		ref = action.daycount({'site': 'test', 'tag': '#test', 'search_body': 'test'})
		self.assertEqual('[{"dummy": "called mock daycount test #test test"}]', ref)

	@mock.patch('niascape.action.basedata')
	def test_tag_count(self, moc):
		self.assertTrue(hasattr(basedata, '_tag_count'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # PENDING 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock _tag_count {site}".strip())]

		moc._tag_count = method

		ref = action.tagcount({})
		self.assertEqual('[{"dummy": "called mock _tag_count"}]', ref)

		ref = action.tagcount({'site': 'test'})
		self.assertEqual('[{"dummy": "called mock _tag_count test"}]', ref)

	@mock.patch('niascape.action.basedata')
	def test_timeline(self, moc):
		self.assertTrue(hasattr(basedata, 'get_all'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # PENDING 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock get_all {site}".strip())]

		moc.get_all = method

		ref = action.timeline({})
		self.assertEqual('[{"dummy": "called mock get_all"}]', ref)

	@skip("モックなし確認用")
	def test_daycount_no_mock(self):
		ini = niascape._read_ini('config.ini')
		niascape.ini = ini
		ref = action.daycount({'site': 'test', 'tag': '#test'})
		self.assertEqual('[{"date": "2016-12-30", "count": 1}, {"date": "2016-10-26", "count": 1}, {"date": "2015-07-10", "count": 1}]', ref)
