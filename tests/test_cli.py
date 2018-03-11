from unittest import TestCase

import sys

import niascape


class TestCli(TestCase):
	def test_cli(self):
		ret = niascape.cli()
		self.assertEqual('top', ret)

		sys.argv.append('hoge')
		ret = niascape.cli()
		self.assertEqual('No Action', ret)
