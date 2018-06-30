from unittest import TestCase, mock, skip

import niascape
from niascape import usecase
from niascape.repository import site
from niascape.utility.database import Database


class TestUsecase(TestCase):
	@classmethod
	def setUpClass(cls):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini

	def test_top(self):
		ret = usecase.top({})
		self.assertEqual('top', ret)

	@mock.patch('niascape.usecase.site.site')
	def test_list(self, moc):
		self.assertTrue(hasattr(site, 'sites'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return f"called mock sites {site}".strip()

		moc.sites = method

		ref = usecase.site.list({})
		self.assertEqual('called mock sites', ref)

	@mock.patch('niascape.usecase.site.site')
	def test_formbottominsert(self, moc):
		self.assertTrue(hasattr(site, 'setting'))  # モックだと関数名の修正についていけないのでチェック

		def method(conn, site=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			if site == 'test':
				return {'siteinsert': 'dummy'}
			else:
				return {'hoge': 'piyo'}

		moc.setting = method

		ref = usecase.site.formbottominsert({})
		self.assertEqual({'siteinsert': ''}, ref)

		ref = usecase.site.formbottominsert({'site': 'test'})
		self.assertEqual({'siteinsert': 'dummy'}, ref)

		ref = usecase.site.formbottominsert({'site': 'aaa'})
		self.assertEqual({'siteinsert': ''}, ref)
