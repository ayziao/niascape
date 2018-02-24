"""
テスト全実行

testsディレクトリ内(サブディレクトリも)のtest_*.pyを実行

主に coverage 向け
  - coverage run --branch --source=niascape tests/all_test.py

"""

import os
import sys
import types
import unittest
from importlib.machinery import SourceFileLoader

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path.rstrip('tests'))

def call_recursive_directory(func: types.FunctionType, directory_name: str) -> None:
	"""
	再帰的にディレクトリ内のファイルに処理を行う
	@param func: function(file_path: str) ファイルに対して何らかの処理を行うファイルパス文字列を引数に持つ関数オブジェクト
	@param directory_name: ディレクトリパス文字列
	"""
	# translationME クラス説明英語化
	for basename in os.listdir(directory_name):
		path = os.path.join(directory_name, basename)
		if not basename.startswith('_'):  # PENDING 処理対象外ファイル、ディレクトリ名のチェック関数も受け取るか
			if os.path.isdir(path):  # ディレクトリの場合は更に掘る
				call_recursive_directory(func, path)
			elif os.path.isfile(path):
				func(path)


def run() -> None:
	"""
	実行
	"""
	suite = unittest.TestSuite()
	test_loader = unittest.TestLoader()

	def _add_test(path_):
		"""
		テストスイート追加

		与えられたファイルパスがtest_なんとか.pyならテストスイートに追加
		:param path_:
		"""
		file = os.path.basename(path_)
		if file.startswith('test_') and file.endswith('.py'):
			# mod = SourceFileLoader(file, path_)  # 3.3未満
			file_loader = SourceFileLoader(os.path.splitext(file)[0], path_)
			mod = file_loader.load_module()
			suite.addTest(test_loader.loadTestsFromModule(mod))

	call_recursive_directory(_add_test, os.path.curdir)  # ディレクトリ内(サブディレクトリ含む)のファイルに実行

	unittest.TextTestRunner(verbosity=2).run(suite)  # テスト実行


if __name__ == "__main__":
	run()
