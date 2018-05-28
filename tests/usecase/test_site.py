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

	@mock.patch('niascape.usecase.site.basedata')
	def test_list(self, moc):
		self.assertTrue(hasattr(basedata, '_sites'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock _sites {site}".strip())]

		moc._sites = method

		ref = usecase.site.list({})
		self.assertEqual('[{"dummy": "called mock _sites"}]', ref)

