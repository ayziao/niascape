from unittest import TestCase

import logging.config

# import json ; logging.addLevelName(5, 'TRACE') ; logging.config.dictConfig(json.load(open('logger_config.json', 'r')))
logger = logging.getLogger(__name__)

import niascape


class TestMyPackage(TestCase):
	def test_main(self):
		ref = niascape.main([])
		self.assertEqual('"top"', ref)

		ref = niascape.main('top')
		self.assertEqual('No Action', ref)

		# モジュール変数をうっかり呼ばないか
		ref = niascape.main('basedata')
		self.assertEqual('No Action', ref)
		ref = niascape.main('json')
		self.assertEqual('No Action', ref)

	def test_main_no_action(self):
		with self.assertLogs('niascape', level='INFO') as cm:
			ref = niascape.main(['hoge'])
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

	def test_main_media(self):
		ref = niascape.main([],{'media_type':'json'})
		self.assertEqual('"top"', ref)

		ref = niascape.main([],{'media_type':'xml'})
		self.assertEqual('media err', ref)

