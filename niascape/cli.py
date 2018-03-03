#!/usr/bin/env pypy3
"""
コマンドラインインターフェース
"""


def cli():
	# TODO コマンドライン引数を解決してニアスケイプRUNを実行して結果をよしなに出力
	import niascape
	return niascape.run()


if __name__ == '__main__':
	import os
	import sys

	# PENDING OSへパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # pragma: no cover
	print(cli())  # pragma: no cover
