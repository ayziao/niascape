from unittest import TestCase

import niascape


class TestMyPackage(TestCase):
	def test_run(self):
		ref = niascape.run()
		self.assertEqual('top', ref)

		ref = niascape.run('top')
		self.assertEqual('top', ref)

		# モジュール変数をうっかり呼ばないか
		ref = niascape.run('basedata')
		self.assertEqual('No Action', ref)
		ref = niascape.run('json')
		self.assertEqual('No Action', ref)

	def test_run_no_action(self):
		with self.assertLogs('niascape', level='INFO') as cm:
			ref = niascape.run('hoge')
			self.assertEqual('No Action', ref)
		self.assertEqual(cm.output, ['INFO:niascape:アクションなし: hoge'])

	def test_read_ini(self):
		ini = niascape._read_ini('config.ini.sample')
		self.assertEqual(['postgresql'], ini.sections())
