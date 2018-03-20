from unittest import TestCase

import sys

from niascape import cli


class TestCli(TestCase):
	def test_cli(self):
		ret = cli.run(['script'])
		self.assertEqual('top', ret)

		ret = cli.run(['script','hoge'])
		self.assertEqual('No Action', ret)

	def test_parse(self):
		ret = cli.parse(['script'])
		self.assertEqual([['script'], {}, []], ret)

		ret = cli.parse(['script', '--option'])
		self.assertEqual([['script'], {'option': True}, []], ret)

		argv = ['script', 'sub_command', 'path', '--option1', '--option2', 'hoge', '--option3=piyo', '-als', '-u']
		ret = cli.parse(argv)
		self.assertEqual([['script', 'sub_command', 'path'], {'option1': True, 'option2': 'hoge', 'option3': 'piyo'}, ['als', 'u']], ret)

# ret = parse(sys.argv)
# self.assertEqual(sys.argv,ret)
