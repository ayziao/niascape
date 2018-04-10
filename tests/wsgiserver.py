"""
# WSGIサーバ 開発用
# 本番環境ではuWSGIとか使ってApacheとかnginxでやりましょう
"""
import os
import sys
import json
from wsgiref import simple_server

import logging.config

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

import niascape
from niascape import wsgiclient


def make_server():
	"""
	# WSGIサーバ起動
	"""
	server = simple_server.make_server('', 8080, wsgiclient.application)
	server.serve_forever()


if __name__ == '__main__':
	with open(path + '/tests/logger_config.json', 'r') as fp:
		logging.config.dictConfig(json.load(fp))
	logger = logging.getLogger(__name__)
	logger.debug("開始時刻(UTC): %s", niascape.init_time)

	make_server()
