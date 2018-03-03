from unittest import TestCase

import niascape


class TestMyapp(TestCase):
	def test_main(self):
		# print(niascape.init_time)
		ref = niascape.run()
		self.assertEqual(ref, 'main')

	def test_loadini(self):
		ini = niascape._readini('config.ini.sample')
		self.assertEqual(['postgresql'], ini.sections())
	# self.assertEqual(ini.sections(), niascape.ini.sections())
