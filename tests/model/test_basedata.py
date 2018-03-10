import logging
import unittest
from pprint import pformat

import niascape
from niascape.model import basedata

logger = logging.getLogger(__name__)


class TestBasedata(unittest.TestCase):

	@unittest.skip("データベース関連のテストを保留")  # TODO データベースに接続してのテストについて考える
	def test_daycount(self):
		ini = niascape._readini('config.ini.sample')
		niascape.ini = ini
		ref = basedata._daycount()

		logger.debug("日別投稿数\n%s", pformat(ref))
		self.assertEqual({'Date': '2018-02-18', 'count': 2}, ref[0])
