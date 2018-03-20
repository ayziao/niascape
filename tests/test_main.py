from unittest import TestCase

import niascape


class TestMyapp(TestCase):
	def test_main(self):
		ref = niascape.run()
		self.assertEqual('top', ref)

		ref = niascape.run('top')
		self.assertEqual('top', ref)

		ref = niascape.run('hoge')
		self.assertEqual('No Action', ref)

		# モジュール変数をうっかり呼ばないか
		ref = niascape.run('basedata')
		self.assertEqual('No Action', ref)
		ref = niascape.run('json')
		self.assertEqual('No Action', ref)

	def test_read_ini(self):
		ini = niascape._read_ini('config.ini.sample')
		self.assertEqual(['postgresql'], ini.sections())
