import unittest
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path.rstrip('tests'))

import niascape


class TestMyapp(unittest.TestCase):
	def test_main(self):
		ref = niascape.run()
		self.assertEqual(ref, 'main')

	# noinspection PyTypeChecker
	def test_wsgiclient_root(self):
		ret = ''
		env = {'PATH_INFO': '/'}
		rethed = ''

		def wsgi(status: str, header: list):
			nonlocal ret, rethed
			ret = status
			rethed = header

		niascape.application(env, wsgi)

		self.assertEqual(ret, '200 OK')
		self.assertEqual(rethed, [('Content-Type', 'text/html; charset=utf-8')])

	# noinspection PyTypeChecker
	def test_wsgiclient_favicon(self):
		ret = ''
		env = {'PATH_INFO': '/favicon.ico'}
		rethed = ''

		def wsgi(status: str, header: list):
			nonlocal ret, rethed
			ret = status
			rethed = header

		niascape.application(env, wsgi)

		self.assertEqual(ret, '404 Not Found')
		self.assertEqual(rethed, [('Content-Type', 'text/html; charset=utf-8')])
