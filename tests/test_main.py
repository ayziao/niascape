from unittest import TestCase
from unittest import mock

import niascape


class TestMyapp(TestCase):
	def test_main(self):
		ref = niascape.run()
		self.assertEqual('top', ref)

		ref = niascape.run('top')
		self.assertEqual('top', ref)

		ref = niascape.run('hoge')
		self.assertEqual('No Action', ref)

		ref = niascape.run('basedata')
		self.assertEqual('No Action', ref)

		ref = niascape.run('json')
		self.assertEqual('No Action', ref)

	def test_loadini(self):
		ini = niascape._readini('config.ini.sample')
		self.assertEqual(['postgresql'], ini.sections())
