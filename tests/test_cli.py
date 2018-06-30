from unittest import TestCase

from niascape import cli


class TestCli(TestCase):
	def test_cli(self):
		ret = cli.run(['script'])
		self.assertEqual('"top"', ret)

		ret = cli.run(['script', 'hoge'])
		self.assertEqual('No Action', ret)

	def test_parse(self):
		ret = cli.parse_argument_vector(['script'])
		self.assertEqual(([], {}, []), ret)

		ret = cli.parse_argument_vector(['script', 'action'])
		self.assertEqual((['action'], {}, []), ret)

		ret = cli.parse_argument_vector(['script', 'action', '--option'])
		self.assertEqual((['action'], {'option': True}, []), ret)

		ret = cli.parse_argument_vector(['script', 'action', '--option', '1'])
		self.assertEqual((['action'], {'option': '1'}, []), ret) # self.assertEqual((['action'], {'option': 1}, []), ret)

		ret = cli.parse_argument_vector(['script', 'action', '--option=1'])
		self.assertEqual((['action'], {'option': '1'}, []), ret) # self.assertEqual((['action'], {'option': 1}, []), ret)

		argv = ['script', 'action', 'sub_command', 'path', '--option1', '--option2', 'foo', '--option3=bar', '-als', '-u']
		ret = cli.parse_argument_vector(argv)
		self.assertEqual((['action', 'sub_command', 'path'], {'option1': True, 'option2': 'foo', 'option3': 'bar'}, ['als', 'u']), ret)

	def test_cast(self):
		ret = cli._cast('1')
		self.assertEqual(1,ret)
		ret = cli._cast('a')
		self.assertEqual('a',ret)
