#!/usr/bin/env pypy3
"""
コマンドラインインターフェース
"""


def cli():
	# TODO コマンドライン引数を解決してニアスケイプRUNを実行して結果をよしなに出力
	import niascape
	return niascape.run()


if __name__ == '__main__': # pragma: no cover
	import os 
	import sys

	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	print(cli())
