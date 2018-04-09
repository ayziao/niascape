from unittest import TestCase

from niascape import cli


class TestCli(TestCase):
	def test_cli(self):
		ret = cli.run(['script'])
		self.assertEqual('top', ret)

		ret = cli.run(['script', 'hoge'])
		self.assertEqual('No Action', ret)

	def test_parse(self):
		ret = cli.parse_argument_vector(['script'])
		self.assertEqual((['script'], {}, []), ret)

		ret = cli.parse_argument_vector(['script', '--option'])
		self.assertEqual((['script'], {'option': True}, []), ret)

		ret = cli.parse_argument_vector(['script', '--option', '1'])
		self.assertEqual((['script'], {'option': 1}, []), ret)

		ret = cli.parse_argument_vector(['script', '--option=1'])
		self.assertEqual((['script'], {'option': 1}, []), ret)

		argv = ['script', 'sub_command', 'path', '--option1', '--option2', 'foo', '--option3=bar', '-als', '-u']
		ret = cli.parse_argument_vector(argv)
		self.assertEqual((['script', 'sub_command', 'path'], {'option1': True, 'option2': 'foo', 'option3': 'bar'}, ['als', 'u']), ret)
