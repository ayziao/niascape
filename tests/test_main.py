
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


	def test_wsgiclient_root(self):
		ret = ['']
		env = {'PATH_INFO':'/'}
		def wsgi(status: str, header:list):
			ret[0] = status
		niascape.application(env,wsgi)

		self.assertEqual(ret[0], '200 OK')

	def test_wsgiclient_favicon(self):
		ret = ['']
		env = {'PATH_INFO':'/favicon.ico'}
		def wsgi(status: str, header:list):
			ret[0] = status
		niascape.application(env,wsgi)

		self.assertEqual(ret[0], '404 Not Found')





