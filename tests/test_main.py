
import unittest
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path.rstrip('/tests'))

import niascape

class TestMyapp(unittest.TestCase):

	def test_main(self):
		ref = niascape.run()
		self.assertEqual(ref, 'main')