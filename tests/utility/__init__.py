from unittest import TestCase

from niascape import utility


class TestUtility(TestCase):

	def test_dynamic_get_method(self):
		method = utility.dynamic_get_method('niascape', 'main')
		self.assertEqual('No Action', method('hoge'))

		ref = utility.dynamic_get_method('niascape.usecase', 'timeline')
		self.assertTrue(callable(ref))

		ref = utility.dynamic_get_method('niascape.usecase', 'postcount.day')
		self.assertTrue(callable(ref))

		ref = utility.dynamic_get_method('niascape.usecase', 'hoge') # 存在しない
		self.assertEqual(None, ref)

		ref = utility.dynamic_get_method('niascape.usecase', 'basedata') # callableでない
		self.assertEqual(None, ref)




