from unittest import TestCase, mock, skip

import niascape
from niascape import usecase
from niascape.repository import basedata
from niascape.utility.database import Database


class Dummy:
	def __init__(self, dummy):
		self.dummy = dummy

	def _asdict(self):
		return {'dummy': self.dummy}


class TestUsecase(TestCase):
	@classmethod
	def setUpClass(cls):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini

	def test_top(self):
		ret = usecase.top({})
		self.assertEqual('top', ret)

	@mock.patch('niascape.usecase.basedata')
	def test_timeline(self, moc):
		self.assertTrue(hasattr(basedata, 'get_all'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock get_all {site}".strip())]

		moc.get_all = method

		ref = usecase.timeline({})
		self.assertEqual('[{"dummy": "called mock get_all"}]', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_tagtimeline(self, moc):
		self.assertTrue(hasattr(basedata, 'tagtimeline'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock tagtimeline {site}".strip())]

		moc.tagtimeline = method

		ref = usecase.tagtimeline({})
		self.assertEqual('[{"dummy": "called mock tagtimeline"}]', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_search_body(self, moc):
		self.assertTrue(hasattr(basedata, 'search_body'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock search_body {site}".strip())]

		moc.search_body = method

		ref = usecase.searchbody({})
		self.assertEqual('[{"dummy": "called mock search_body"}]', ref)
