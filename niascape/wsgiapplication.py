"""
niascape.wsgiapplication
"""
from typing import Callable

import logging
from pprint import pformat

logger = logging.getLogger(__name__)

import niascape


def application(environ: dict, start_response: Callable[[str, list], None]):
	"""
	# WSGI application
	#
	# WSGIサーバから呼ばれるところ
	@param environ: webサーバ環境変数等
	@param start_response: レスポンス コールバック関数  function(status: str, header: [(key: str,value: str), ...])
	"""
	logger.debug("environ: \n%s", pformat(environ))

	if environ['PATH_INFO'] == '/favicon.ico':
		# PENDING 拒否リスト作る
		# PENDING ファビコンどうするか
		start_response('404 Not Found', [('Content-Type', 'text/plain; charset=utf-8')])
		yield 'Not Found'.encode()

	else:
		html = """
		<html>
			<head>
				<meta content="text/html charset=UTF-8" http-equiv="Content-Type"/>
				<title>たいとる</title>
			</head>
			<body>
				<p>{body}</p>
			</body>
		</html>
		"""

		body = niascape.run()
		html = html.replace('\n', '').replace('\t', '').format(body=body)

		start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		yield html.encode()
