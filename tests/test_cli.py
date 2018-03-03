from unittest import TestCase

from niascape import cli


class TestCli(TestCase):
	def test_cli(self):
		ret = cli.cli()
		self.assertEqual('main', ret)
