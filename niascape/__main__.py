"""
コマンドライン起動をディレクトリでやったときのためだけのところ

使い方
$ python3 niascape action
$ pypy3 niascape action
"""
if __name__ == '__main__':  # pragma: no cover
	import datetime

	time = datetime.datetime.utcnow()

	import os
	import sys

	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(path)  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	import logging.config
	import json

	logging.addLevelName(5, 'TRACE')  # PENDING 独自拡張ロギングをユーティリティ辺りに作るか検討
	logging.config.dictConfig(json.load(open(path + '/logger_config.json', 'r')))  # TODO デバッグ表示を運用用と実装用にどうにか
	logger = logging.getLogger(__name__)

	from niascape import cli, init_time

	logger.log(5, "開始時刻(UTC): %s", time)
	logger.log(5, "開始時刻(UTC): %s", init_time)

	logger.log(5, "実行中のスクリプトへの相対パス: %s", __file__)
	logger.log(5, "実行中のスクリプトへの絶対パス: %s", os.path.abspath(__file__))

	# sys.argv.extend("nothing_action".split())
	# sys.argv.extend("postcount.day --site=test --tag=#test test".split())
	# sys.argv.extend("postcount.tag --site=test".split())
	# sys.argv.extend("timeline --site=test --page=2".split())

	print(cli.run(sys.argv))

	# ret = json.loads(cli.run(sys.argv))
	# print(len(ret))
	# pprint(ret)

	logger.log(5, "終了時刻(UTC): %s", datetime.datetime.utcnow())
