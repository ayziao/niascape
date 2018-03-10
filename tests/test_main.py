import unittest
from unittest import TestCase

import niascape


class TestMyapp(TestCase):
	def test_main(self):
		ref = niascape.run()
		self.assertEqual('top', ref)

	def test_loadini(self):
		ini = niascape._readini('config.ini.sample')
		self.assertEqual(['postgresql'], ini.sections())

	@unittest.skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_daycount(self):
		ini = niascape._readini('config.ini.sample')
		niascape.ini = ini
		ref = niascape.__main__._daycount()
		self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
