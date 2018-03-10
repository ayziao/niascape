from unittest import TestCase

import sys

from niascape import cli


class TestCli(TestCase):
	def test_cli(self):
		ret = cli.cli()
		self.assertEqual('top', ret)

		sys.argv.append('hoge')
		ret = cli.cli()
		self.assertEqual('No Action', ret)
