from unittest import TestCase
from unittest import mock

from niascape.wsgiclient import application, parse_query_string

import logging

logger = logging.getLogger(__name__)


# logging.basicConfig(format='\033[0;32m%(asctime)s %(levelname)5s \033[0;34m%(message)s \033[0;32m(%(name)s.%(funcName)s) \033[0m', level=logging.DEBUG)  # PENDING リリースとデバッグ切り替えどうしようか logging.conf調べる


class TestWsgiclient(TestCase):

	def test_application_root(self):
		env = {'PATH_INFO': '/', 'QUERY_STRING': ''}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		ret_content += application(env, wsgi).__next__()

		# PENDING 本文アサートどうするか
		self.assertEqual('200 OK', ret_stat)
		self.assertEqual([('Content-Type', 'text/html; charset=utf-8')], ret_hed)

	def test_application_favicon(self):
		env = {'PATH_INFO': '/favicon.ico'}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		for a in application(env, wsgi):
			ret_content += a

		self.assertEqual('404 Not Found', ret_stat)
		self.assertEqual([('Content-Type', 'text/plain; charset=utf-8')], ret_hed)
		self.assertEqual(b'Not Found', ret_content)

	def test_parse_query_string(self):
		ret = parse_query_string('blank_value&key=value&sharp=%23hoge&list[]=1&list[]=2&list[]=3')
		self.assertEqual({'key': 'value', 'list': ['1', '2', '3'], 'sharp': '#hoge'}, ret)

		ret = parse_query_string('blank_value&key=value&sharp=%23hoge&list[]=1&list[]=2&list[]=3', True)
		self.assertEqual({'blank_value': '', 'key': 'value', 'list': ['1', '2', '3'], 'sharp': '#hoge'}, ret)

		ret = parse_query_string('blank_value&blank_value2&key=value&sharp=%23hoge&list[]=1&list[]=2&list[]=3', True)
		self.assertEqual({'blank_value': '', 'blank_value2': '', 'key': 'value', 'list': ['1', '2', '3'], 'sharp': '#hoge'}, ret)

	@mock.patch('niascape.action.basedata')
	def test_daycount(self, moc):
		def method(conn, site='', tag='', search_body=''):  # PENDING 引数の定義を実装から動的にパクれないか inspectモジュール？
			return [Dummy(f"called mock daycount {site} {tag} {search_body}".strip())]

		moc._daycount = method

		env = {'PATH_INFO': '', 'QUERY_STRING': 'daycount&tag=test'}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		ret_content += application(env, wsgi).__next__()

		# PENDING 本文アサートどうするか
		self.assertEqual('200 OK', ret_stat)
		self.assertEqual([('Content-Type', 'text/json; charset=utf-8')], ret_hed)


class Dummy:
	def __init__(self, dummy):
		self.dummy = dummy

	def _asdict(self):
		return self.dummy
