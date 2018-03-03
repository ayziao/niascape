"""
メインモジュール

# TODO メインモジュールの説明書く
"""


def run() -> str:
	return 'main'


if __name__ == '__main__':
	import os  # pragma: no cover
	import sys # pragma: no cover

	# PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # pragma: no cover
	from niascape import cli  # pragma: no cover

	print(cli.cli())  # pragma: no cover
