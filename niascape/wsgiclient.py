"""
niascape.wsgiapplication
"""
from typing import Callable, List, Tuple, Generator, Dict, Union ,Any
from urllib.parse import parse_qsl

import logging
from pprint import pformat

logger = logging.getLogger(__name__)

import niascape


def application(environ: dict, start_response: Callable[[str, List[Tuple[str, str]]], None]) -> Generator:
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
		parsed = _parse(environ)  # parse_query_string(environ['QUERY_STRING'], True)
		arguments = parsed[0]
		option_dict = parsed[1]

		logger.debug("parsed: \n%s", pformat(parsed))

		if len(arguments) > 0:
			action_name = arguments[0]
		else:
			action_name = 'top'

		content = niascape.run(action_name, option_dict)

		if action_name == 'top' or content == 'No Action':
			html = """
			<html>
				<head>
					<meta content="text/html charset=UTF-8" http-equiv="Content-Type"/>
					<title>{title}</title>
				</head>
				<body>
					<p>{body}</p>
				</body>
			</html>
			"""
			content = html.replace('\n', '').replace('\t', '').format(body=content, title=action_name)
			start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		else:
			start_response('200 OK', [('Content-Type', 'text/json; charset=utf-8')])

		yield content.encode()


def parse_query_string(query_string: str, keep_blank_values: bool = False) -> Dict[str,Union[str,List[str]]]:
	"""
	urllib.parse.parse_qs が全部リストで値を返すので[]だけリストになるよう自作
	# PENDING 逆にCLIパーサーをオプション値を全部リストにすべき？
	"""
	query_list = parse_qsl(query_string, keep_blank_values=keep_blank_values)
	query_dict = {}  # type: Dict[str,Any]  # XXX Dict[str,Union[str,List[str]]] にしたい 文字列にアペンドなんてねーよってマイパイさんにいわれる

	for key, query in query_list:
		if '[]' in key:
			key = key.rstrip('[]')
			if key in query_dict.keys():
				query_dict[key].append(query)
			else:
				query_dict[key] = [query]
		else:
			query_dict[key] = query

	logger.debug("query_string: \n%s", pformat(query_string))
	logger.debug("query_list: \n%s", pformat(query_list))
	logger.debug("query_dict: \n%s", pformat(query_dict))

	return query_dict


def _parse(environ: dict) -> Tuple[List[str], dict]:
	arguments = []
	option_dict = {}

	query_dict = parse_query_string(environ['QUERY_STRING'], True)

	for key, value in query_dict.items():
		if value == '':
			arguments.append(key)
		else:
			option_dict[key] = value

	path_list = environ['PATH_INFO'].split('/')

	logger.debug("path: \n%s", path_list)

	if len(path_list) > 1:
		option_dict['site'] = path_list[1]
	else:
		option_dict['site'] = ''

	return arguments, option_dict


if __name__ == '__main__':  # pragma: no cover
	# logging.basicConfig(level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる
	logging.basicConfig(format='\033[0;32m%(asctime)s %(name)s %(funcName)s\033[0;34m\n[%(levelname)s] %(message)s\033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


	def wsgi_start_response(status: str, header: list):
		pass


	env = {'PATH_INFO': '/test/', 'QUERY_STRING': 'daycount&tag=%23test&search_body=test'}
	ret = application(env, wsgi_start_response).__next__()
	print(ret)
