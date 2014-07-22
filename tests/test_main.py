
import unittest
from niascape.main import main

class TestMyapp(unittest.TestCase):

	def test_main(self):
		ref = main()
		self.assertEqual(ref, 'main')