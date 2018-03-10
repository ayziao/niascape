from unittest import TestCase
from unittest import mock

import niascape
from niascape.model import basedata


class TestMyapp(TestCase):
	def test_main(self):
		ref = niascape.run()
		self.assertEqual('top', ref)

		ref = niascape.run('top')
		self.assertEqual('top', ref)

		ref = niascape.run('hoge')
		self.assertEqual('No Action', ref)

	def test_loadini(self):
		ini = niascape._readini('config.ini.sample')
		self.assertEqual(['postgresql'], ini.sections())

	@mock.patch('niascape.__main__.basedata')
	def test_main_daycount(self, moc):
		def method():
			return [{'Date': '2016-12-30', 'count': 1}, {'Date': '2016-10-26', 'count': 1}]

		self.assertTrue(hasattr(basedata, '_daycount'))
		moc._daycount = method

		ref = niascape.run('daycount')
		self.assertEqual('[{"Date": "2016-12-30", "count": 1}, {"Date": "2016-10-26", "count": 1}]', ref)
