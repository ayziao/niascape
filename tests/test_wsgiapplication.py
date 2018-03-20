from unittest import TestCase

import niascape


class TestWsgiapplication(TestCase):

	def test_wsgiclient_root(self):
		ret = ''
		env = {'PATH_INFO': '/'}
		ret_hed = ''

		def wsgi(status: str, header: list):
			nonlocal ret, ret_hed
			ret = status
			ret_hed = header

		niascape.application(env, wsgi)

		self.assertEqual(ret, '200 OK')
		self.assertEqual(ret_hed, [('Content-Type', 'text/html; charset=utf-8')])

	def test_wsgiclient_favicon(self):
		ret = ''
		env = {'PATH_INFO': '/favicon.ico'}
		ret_hed = ''

		def wsgi(status: str, header: list):
			nonlocal ret, ret_hed
			ret = status
			ret_hed = header

		niascape.application(env, wsgi)

		self.assertEqual(ret, '404 Not Found')
		self.assertEqual(ret_hed, [('Content-Type', 'text/html; charset=utf-8')])
