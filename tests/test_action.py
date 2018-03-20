import unittest
from unittest import mock

from niascape import action
from niascape.entity import basedata


class TestAction(unittest.TestCase):
	def test_top(self):
		ret = action.top({})
		self.assertEqual('top', ret)

	@mock.patch('niascape.action.basedata')
	def test_daycount(self, moc):
		self.assertTrue(hasattr(basedata, '_daycount'))  # モックだと関数名の修正についていけないのでチェック

		def method(site='', tag='', search_body=''):  # PENDING 引数の定義を実装から動的にパクれないか inspectモジュール？
			return f"called mock daycount {site} {tag} {search_body}".strip()

		moc._daycount = method

		ref = action.daycount({})
		self.assertEqual('"called mock daycount"', ref)

		ref = action.daycount({'site': 'test', 'tag': '#test', 'search_body': 'test'})
		self.assertEqual('"called mock daycount test #test test"', ref)
