"""
コマンドライン起動をディレクトリでやったときのためだけのところ
"""
if __name__ == '__main__':  # pragma: no cover
	import os
	import sys
	import datetime

	import logging

	logger = logging.getLogger(__name__)
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	from niascape import cli, init_time

	logging.basicConfig(format='\033[0;32m%(asctime)s %(name)s %(funcName)s\033[0;34m\n[%(levelname)s] %(message)s\033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる

	logger.debug("開始時刻(UTC): %s", init_time)

	logger.debug("実行中のスクリプトへの相対パス: %s", __file__)
	logger.debug("実行中のスクリプトへの絶対パス: %s", os.path.abspath(__file__))

	# sys.argv.extend("hoge test #test test".split())

	print(cli.run(sys.argv))

	logger.debug("終了時刻(UTC): %s", datetime.datetime.utcnow())
