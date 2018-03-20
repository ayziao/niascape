from unittest import TestCase

import sys

import niascape
from niascape.cli import parse

class TestCli(TestCase):
	def test_cli(self):
		ret = niascape.cli()
		self.assertEqual('top', ret)

		sys.argv.append('hoge')
		ret = niascape.cli()
		self.assertEqual('No Action', ret)

	def test_parse(self):
		argv = ['script','sub_command', 'path', '--option1', '--option2', 'hoge', '--option3=piyo', '-als', 'gfgfg' ,'-u']
		ret = parse(argv)
		
		self.assertEqual([['script', 'sub_command', 'path', 'gfgfg'], {'option1': True, 'option2': 'hoge', 'option3': 'piyo'}, ['als','u']],ret)
		
		# ret = parse(sys.argv)
		# self.assertEqual(sys.argv,ret)

