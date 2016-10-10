"""
# WSGIサーバ 開発用
# 本番環境ではApacheとかnginxとか使いましょう
"""
import sys
import os
from wsgiref import simple_server

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path.rstrip('tests'))

import niascape


def make_server():
	"""
	# WSGIサーバ起動
	"""
	server = simple_server.make_server('', 8080, niascape.application)
	server.serve_forever()


if __name__ == '__main__':
	make_server()