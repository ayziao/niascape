"""
メインモジュール

# TODO メインモジュールの説明書く
"""


def run() -> str:
	return 'main'


if __name__ == '__main__': # pragma: no cover
	import os 
	import sys

	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 	# PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	from niascape import cli

	print(cli.cli())
