from unittest import TestCase

import niascape


class TestWsgiapplication(TestCase):

	def test_wsgiclient_root(self):
		env = {'PATH_INFO': '/'}
		ret_stat = ''
		ret_hed = ''
		ret_content = b''

		def wsgi(status: str, header: list):
			nonlocal ret_stat, ret_hed
			ret_stat = status
			ret_hed = header

		niascape.application(env, wsgi).__next__()

		self.assertEqual('200 OK', ret_stat)
		self.assertEqual([('Content-Type', 'text/html; charset=utf-8')], ret_hed)
		# PENDING 本文アサートどうするか

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
