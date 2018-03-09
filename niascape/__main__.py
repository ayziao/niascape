"""
メインモジュール

# TODO メインモジュールの説明書く
"""
import logging

logger = logging.getLogger(__name__)


def run() -> str:
	return 'main'


if __name__ == '__main__':  # pragma: no cover
	import os
	import sys

	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	from niascape import cli

	logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	logger.debug(__file__)
	# logger.debug(os.path.abspath(__file__))

	print(cli.cli())
