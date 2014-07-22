"""
テスト全実行

testsディレクトリ内(サブディレクトリも)のtest_なんとか.pyを実行

  - coverage run --branch --source=niascape tests/all_test.py

"""

import sys
import os
import imp
from types import FunctionType
import unittest

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path.rstrip('tests'))


def call_recursive_directory(func: FunctionType, dir_: str) -> None:
	"""
	再帰的にディレクトリ内のファイルに処理を行う
	@param func: function(file_path: str) ファイルパス文字列を引数に持つ関数オブジェクト
	@param dir_: ディレクトリパス文字列
	"""
	#translationME クラス説明英語化
	for basename in os.listdir(dir_):
		path = os.path.join(dir_, basename)
		if not basename.startswith('_'):  # PENDING 処理対象外ファイル、ディレクトリ名のチェック関数も受け取るか
			if os.path.isdir(path):
				call_recursive_directory(func, path)
			elif os.path.isfile(path):
				func(path)


def run() -> None:
	"""
	実行
	"""
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()

	#ディレクトリ内のtest_なんとか.pyをテストスイートに追加
	def _add_test(path_):
		file = os.path.basename(path_)
		if file.startswith('test_') and file.endswith('.py'):
			mod = imp.load_source(os.path.splitext(file)[0], path_)
			suite.addTest(loader.loadTestsFromModule(mod))

	call_recursive_directory(_add_test, os.path.curdir) #ディレクトリ内(サブディレクトリ含む)のファイルに実行

	unittest.TextTestRunner(verbosity=2).run(suite) #テスト実行


if __name__ == "__main__":
	run()
