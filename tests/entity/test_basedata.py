import unittest

import logging
from pprint import pformat

logger = logging.getLogger(__name__)

import niascape
from niascape.entity import basedata


class TestBasedata(unittest.TestCase):

	@unittest.skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_daycount(self):
		ini = niascape._read_ini('config.ini.sample')
		niascape.ini = ini
		ref = basedata._daycount()

		logger.debug("日別投稿数\n%s", pformat(ref))
		self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
