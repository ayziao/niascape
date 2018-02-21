"""
メインモジュール

packageの__init__.pyで読み込んでるのでコマンドラインから直接実行する時ぐらいかな
"""

# TODO メインモジュールの説明書く
from types import FunctionType


def run() -> str:
	"""
	# コマンドライン向け
	@return:
	"""
	#
	return 'main'


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
		body = run()
		html = html.strip().format(body=body)
		start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		return [html.encode()]


if __name__ == '__main__':
	print(run())  # pragma: no cover
