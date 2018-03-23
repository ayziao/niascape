from unittest import TestCase
from unittest import mock

import niascape
from niascape.wsgiapplication import parse_query_string


class TestWsgiapplication(TestCase):

	def test_wsgiclient_root(self):
		env = {'PATH_INFO': '/', 'QUERY_STRING': ''}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		niascape.application(env, wsgi).__next__()

		# PENDING 本文アサートどうするか
		self.assertEqual('200 OK', ret_stat)
		self.assertEqual([('Content-Type', 'text/html; charset=utf-8')], ret_hed)

	def test_wsgiclient_favicon(self):
		env = {'PATH_INFO': '/favicon.ico'}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		for a in niascape.application(env, wsgi):
			ret_content += a

		self.assertEqual('404 Not Found', ret_stat)
		self.assertEqual([('Content-Type', 'text/plain; charset=utf-8')], ret_hed)
		self.assertEqual(b'Not Found', ret_content)

	def test_parse_query_string(self):
		ret = parse_query_string('blanc_value&key=value&sharp=%23hoge&list[]=1&list[]=2&list[]=3')
		self.assertEqual({'key': 'value', 'list': ['1', '2', '3'], 'sharp': '#hoge'}, ret)

		ret = parse_query_string('blanc_value&key=value&sharp=%23hoge&list[]=1&list[]=2&list[]=3', True)
		self.assertEqual({'blanc_value': '', 'key': 'value', 'list': ['1', '2', '3'], 'sharp': '#hoge'}, ret)

		ret = parse_query_string('blanc_value&blanc_value2&key=value&sharp=%23hoge&list[]=1&list[]=2&list[]=3', True)
		self.assertEqual({'blanc_value': '', 'blanc_value2': '', 'key': 'value', 'list': ['1', '2', '3'], 'sharp': '#hoge'}, ret)

	@mock.patch('niascape.action.basedata')
	def test_daycount(self, moc):
		def method(site='', tag='', search_body=''):  # PENDING 引数の定義を実装から動的にパクれないか inspectモジュール？
			return [dummy(f"called mock daycount {site} {tag} {search_body}".strip())]

		moc._daycount = method

		env = {'PATH_INFO': '', 'QUERY_STRING': 'daycount&tag=test'}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		niascape.application(env, wsgi).__next__()
		
		# PENDING 本文アサートどうするか
		self.assertEqual('200 OK', ret_stat)
		self.assertEqual([('Content-Type', 'text/json; charset=utf-8')], ret_hed)


class dummy():
	def __init__(self, dummy):
		self.dummy = dummy

	def _asdict(self):
		return self.dummy
