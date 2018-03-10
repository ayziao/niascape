"""
テスト全実行

testsディレクトリ内(サブディレクトリも)のtest*.pyを実行

主に coverage 向け
coverage run --branch --source=niascape tests
"""
import unittest

import os
import sys

import logging
from pprint import pformat

logger = logging.getLogger(__name__)

if __name__ == "__main__":
	verbosity = 1
	if __file__ == "tests":  # coverage 通すとディレクトリ実行時__file__がtests/__main__.pyにならない対策
		path = os.path.abspath(__file__)
	else:
		path = os.path.dirname(os.path.abspath(__file__))
		logging.basicConfig(level=logging.DEBUG)  # coverage通してない時デバッグ情報出す
		if __file__ == "tests/__main__.py":
			verbosity = 2

	logger.debug("カレントディレクトリ:%s", os.getcwd())

	logger.debug("実行中のスクリプトへの相対パス:%s", __file__)
	logger.debug("実行中のスクリプトへの絶対パス:%s", os.path.abspath(__file__))
	logger.debug("Python検索パス:\n%s", pformat(sys.path))

	sys.path.append(os.path.dirname(path))

	logger.debug("Python検索パス追加後:\n%s\n", pformat(sys.path))

	all_tests = unittest.TestLoader().discover(path)
	unittest.TextTestRunner(verbosity=verbosity).run(all_tests)
