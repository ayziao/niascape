import unittest
from unittest import mock

import sys

from niascape import action
from niascape.entity import basedata


class TestAction(unittest.TestCase):
	def test_top(self):
		ret = action.top(None)
		self.assertEqual('top', ret)

	@mock.patch('niascape.action.basedata')
	def test_daycount(self, moc):
		def method(option0, option1, opthion2):
			return 'called mock daycount'

		self.assertTrue(hasattr(basedata, '_daycount'))
		moc._daycount = method

		ref = action.daycount([1, 2, 3])
		self.assertEqual('"called mock daycount"', ref)
