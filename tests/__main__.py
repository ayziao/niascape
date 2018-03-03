"""
テスト全実行

testsディレクトリ内(サブディレクトリも)のtest*.pyを実行

主に coverage 向け
coverage run --branch --source=niascape tests
"""
import os
import sys
import unittest

if __name__ == "__main__":
	# coverage 通すとディレクトリ実行時__file__がtests/__main__.pyにならない対策
	if __file__ == "tests":
		path = os.path.abspath(__file__)
	else:
		path = os.path.dirname(os.path.abspath(__file__))

	sys.path.append(os.path.dirname(path))

	all_tests = unittest.TestLoader().discover(path)
	unittest.TextTestRunner(verbosity=2).run(all_tests)
