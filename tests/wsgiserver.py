"""
# WSGIサーバ 開発用
# 本番環境ではuWSGIとか使ってApacheとかnginxでやりましょう
"""
import os
import sys
from wsgiref import simple_server

import logging

logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # PENDING 実行環境へパッケージとしてインストールすればsys.path.append必要なくなるくさいがどうするか

import niascape
from niascape import wsgiclient


def make_server():
	"""
	# WSGIサーバ起動
	"""
	server = simple_server.make_server('', 8080, wsgiclient.application)
	server.serve_forever()


if __name__ == '__main__':
	logging.basicConfig(format='\033[0;32m%(asctime)s %(name)s %(funcName)s\033[0;34m\n[%(levelname)s] %(message)s\033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	logger.debug("開始時刻(UTC): %s", niascape.init_time)

	make_server()
