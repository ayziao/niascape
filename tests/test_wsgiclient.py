from unittest import TestCase, mock

import logging.config

# import json ; logging.addLevelName(5, 'TRACE') ; logging.config.dictConfig(json.load(open('logger_config.json', 'r')))
logger = logging.getLogger(__name__)

import niascape
from niascape.wsgiclient import application, parse_query_string
from niascape.utility.database import Database


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

		self.assertEqual('200 OK', ret_stat)
		self.assertEqual([('Content-Type', 'text/html; charset=utf-8')], ret_hed)
		self.assertEqual(b'<html><head><meta content="text/html charset=UTF-8" http-equiv="Content-Type"/><title>top</title></head><body><p>top</p></body></html>', ret_content)

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

	@mock.patch('niascape.usecase.postcount.postcount')
	def test_daycount(self, moc):
		niascape.ini = niascape._read_ini('config.ini.sample')  # PENDING テスト用設定読むのどうにかしたい

		def method(conn, site='', tag='', search_body=''):  # XXX 引数の定義を実装から動的にパクれないか inspectモジュール？
			self.assertIsInstance(conn, Database)
			return [Dummy(f"called mock daycount {site} {tag} {search_body}".strip())]

		moc.day = method

		env = {'PATH_INFO': '/test/', 'QUERY_STRING': 'postcount.day&tag=test'}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		ret_content += application(env, wsgi).__next__()

		self.assertEqual('200 OK', ret_stat)
		self.assertEqual([('Content-Type', 'text/json; charset=utf-8')], ret_hed)
		self.assertEqual(b'[{"dummy": "called mock daycount test test"}]', ret_content)


class Dummy:
	def __init__(self, dummy):
		self.dummy = dummy

	def _asdict(self):
		return {'dummy': self.dummy}
