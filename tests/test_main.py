from unittest import TestCase

import niascape

import logging

logger = logging.getLogger(__name__)

# logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


class TestMyPackage(TestCase):
	def test_main(self):
		ref = niascape.main()
		self.assertEqual('top', ref)

		ref = niascape.main('top')
		self.assertEqual('top', ref)

		# モジュール変数をうっかり呼ばないか
		ref = niascape.main('basedata')
		self.assertEqual('No Action', ref)
		ref = niascape.main('json')
		self.assertEqual('No Action', ref)

	def test_main_no_action(self):
		with self.assertLogs('niascape', level='INFO') as cm:
			ref = niascape.main('hoge')
			self.assertEqual('No Action', ref)
		self.assertEqual(cm.output, ['INFO:niascape:アクションなし: hoge'])

	def test_read_ini(self):
		ini = niascape._read_ini('config.ini.sample')
		d = dict(ini)
		logger.debug(ini)
		logger.debug(d)
		logger.debug(d['database'])
		logger.debug(dict(d['database']))
		self.assertEqual('database', ini.sections()[0])
