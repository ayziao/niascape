"""
niascape.wsgiclient
"""
from typing import Callable, List, Tuple, Generator, Dict, Union, Any
from urllib.parse import parse_qsl

import niascape

import logging.config
from pprint import pformat

logger = logging.getLogger(__name__)


def application(environ: dict, start_response: Callable[[str, List[Tuple[str, str]]], None]) -> Generator:
	"""
	WSGI application

	WSGIサーバから呼ばれるところ

	:param environ: webサーバ環境変数等
	:param start_response: レスポンス コールバック関数  function(status: str, header: [(key: str,value: str), ...])
	"""
	logger.log(5, "environ: %s", pformat(environ))

	if environ['PATH_INFO'] == '/favicon.ico':
		# PENDING 拒否リスト作る？
		# PENDING ファビコンどうするか
		start_response('404 Not Found', [('Content-Type', 'text/plain; charset=utf-8')])
		yield 'Not Found'.encode()

	else:
		arguments, option_dict = _parse(environ)

		logger.log(5, "parsed: %s", pformat(arguments))
		logger.log(5, "parsed: %s", pformat(option_dict))

		if len(arguments) > 0:
			action = arguments[0]
		else:
			action = 'top'

		content = niascape.main(action, option_dict)

		if action == 'top' or content == 'No Action':
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
			content = html.replace('\n', '').replace('\t', '').format(body=content, title=action)
			start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		else:
			start_response('200 OK', [('Content-Type', 'text/json; charset=utf-8')])

		yield content.encode()


def parse_query_string(query_string: str, keep_blank_values: bool = False) -> Dict[str, Union[str, List[str]]]:
	"""
	urllib.parse.parse_qs が全部リストで値を返すので[]だけリストになるよう自作

	:param query_string: environ['QUERY_STRING']
	:param keep_blank_values: 値の入っていないフィールドを無視せず空白文字の入ったフィールドとして返すか
	:return: 辞書へパースされたクエリ
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

	logger.log(5, "query_string: %s", pformat(query_string))
	logger.log(5, "query_list  : %s", pformat(query_list))
	logger.log(5, "query_dict  : %s", pformat(query_dict))

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

	path_list = environ['PATH_INFO'].split('/')  # PENDING サブドメインモード？

	logger.log(5, "path: %s", path_list)

	option_dict['site'] = path_list[1]

	# PENDING 変なPATH_INFOが入ることを考慮すべきかどうか
	# if len(path_list) > 1:
	# 	option_dict['site'] = path_list[1]
	# else:
	# 	option_dict['site'] = ''

	return arguments, option_dict


if __name__ == '__main__':  # pragma: no cover
	# import os, json ; logging.config.dictConfig(json.load(pen(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tests/logger_config.json', 'r'))) ; logger = logging.getLogger()

	# noinspection PyUnusedLocal
	def wsgi_start_response(status: str, header: list):
		pass


	env = {'PATH_INFO': '/test/', 'QUERY_STRING': 'postcount.day&tag=%23test&search_body=test'}
	ret = application(env, wsgi_start_response).__next__()
	print(ret)
