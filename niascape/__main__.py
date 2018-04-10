"""
コマンドライン起動をディレクトリでやったときのためだけのところ
"""
if __name__ == '__main__':  # pragma: no cover
	import datetime

	time = datetime.datetime.utcnow()

	import os
	import sys
	import json
	import logging
	from pprint import pprint

	logger = logging.getLogger(__name__)
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる

	from niascape import cli, init_time

	logger.debug("開始時刻(UTC): %s", time)
	logger.debug("開始時刻(UTC): %s", init_time)

	logger.debug("実行中のスクリプトへの相対パス: %s", __file__)
	logger.debug("実行中のスクリプトへの絶対パス: %s", os.path.abspath(__file__))

	# sys.argv.extend("nothing_action".split())
	# sys.argv.extend("daycount --site=test --tag=#test test".split())
	# sys.argv.extend("tagcount --site=test".split())
	sys.argv.extend("timeline --site=test --page=2".split())

	pprint(cli.run(sys.argv))

	ret = json.loads(cli.run(sys.argv))
	print(len(ret))
	pprint(ret)

	logger.debug("終了時刻(UTC): %s", datetime.datetime.utcnow())
