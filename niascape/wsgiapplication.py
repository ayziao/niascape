"""
niascape.wsgiapplication
"""
from types import FunctionType

import niascape


def application(environ: dict, start_response: FunctionType):
	"""
	# WSGI application
	#
	# WSGIサーバから呼ばれるところ
	@param environ: webサーバ環境変数等
	@param start_response: レスポンス コールバック関数  function(status: str, header: [(key: str,value: str), ...])
	"""
	if environ['PATH_INFO'] == '/favicon.ico':
		# PENDING 拒否リスト作る
		# PENDING ファビコンどうするか
		start_response('404 Not Found', [('Content-Type', 'text/html; charset=utf-8')])
		return ['Not Found'.encode()]
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
		html = html.strip().format(body=body)
		start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		return [html.encode()]
