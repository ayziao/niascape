import unittest
import os
import niascape


class TestMyapp(unittest.TestCase):
	def test_main(self):
		# print(niascape.init_time)
		ref = niascape.run()
		self.assertEqual(ref, 'main')


	def test_loadini(self):
		cwd = os.getcwd()

		if 'tests' in cwd: os.chdir(cwd.rstrip('tests'))

		ini = niascape.main.readini('config.ini.sample')
		self.assertEqual(['postgresql'], ini.sections())

		if 'tests' in cwd: os.chdir(cwd)
