"""
# WSGIサーバ 開発用
# 本番環境ではuWSGIとか使ってApacheとかnginxでやりましょう
"""
import os
import sys
import json
from wsgiref import simple_server

import logging.config


def make_server(wsgiapplication):
	"""
	# WSGIサーバ起動
	"""
	server = simple_server.make_server('', 8080, wsgiapplication)
	server.serve_forever()


if __name__ == '__main__':
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(path)  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

	logging.addLevelName(5, 'TRACE')  # PENDING 独自拡張ロギングをユーティリティ辺りに作るか検討
	with open(path + '/tests/logger_config.json', 'r') as fp:
		logging.config.dictConfig(json.load(fp))
	logger = logging.getLogger(__name__)

	import niascape
	from niascape import wsgiclient

	logger.log(5, "開始時刻(UTC): %s", niascape.init_time)

	make_server(wsgiclient.application)
