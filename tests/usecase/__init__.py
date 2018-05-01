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
	def test_tag_count(self, moc):
		self.assertTrue(hasattr(basedata, '_tag_count'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock _tag_count {site}".strip())]

		moc._tag_count = method

		ref = usecase.tagcount({})
		self.assertEqual('[{"dummy": "called mock _tag_count"}]', ref)

		ref = usecase.tagcount({'site': 'test'})
		self.assertEqual('[{"dummy": "called mock _tag_count test"}]', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_sites(self, moc):
		self.assertTrue(hasattr(basedata, '_sites'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock _sites {site}".strip())]

		moc._sites = method

		ref = usecase.sites({})
		self.assertEqual('[{"dummy": "called mock _sites"}]', ref)

	@mock.patch('niascape.usecase.basedata')
	def test_timeline(self, moc):
		self.assertTrue(hasattr(basedata, 'get_all'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock get_all {site}".strip())]

		moc.get_all = method

		ref = usecase.timeline({})
		self.assertEqual('[{"dummy": "called mock get_all"}]', ref)
