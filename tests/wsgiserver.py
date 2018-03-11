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


def make_server():
	"""
	# WSGIサーバ起動
	"""
	server = simple_server.make_server('', 8080, niascape.application)
	server.serve_forever()


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s %(name)s\n[%(levelname)s] %(message)s', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	logger.debug("開始時刻(UTC): %s", niascape.init_time)

	make_server()
