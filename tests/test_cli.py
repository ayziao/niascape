from unittest import TestCase

import sys

import niascape
from niascape.cli import parse


class TestCli(TestCase):
	def test_cli(self):
		ret = niascape.cli(['script'])
		self.assertEqual('top', ret)

		ret = niascape.cli(['script','hoge'])
		self.assertEqual('No Action', ret)

	def test_parse(self):
		ret = parse(['script'])
		self.assertEqual([['script'], {}, []], ret)

		ret = parse(['script', '--option'])
		self.assertEqual([['script'], {'option': True}, []], ret)

		argv = ['script', 'sub_command', 'path', '--option1', '--option2', 'hoge', '--option3=piyo', '-als', '-u']
		ret = parse(argv)
		self.assertEqual([['script', 'sub_command', 'path'], {'option1': True, 'option2': 'hoge', 'option3': 'piyo'}, ['als', 'u']], ret)

# ret = parse(sys.argv)
# self.assertEqual(sys.argv,ret)
