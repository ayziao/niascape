
import unittest
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path.rstrip('/tests'))

from niascape.main import main

class TestMyapp(unittest.TestCase):

	def test_main(self):
		ref = main()
		self.assertEqual(ref, 'main')