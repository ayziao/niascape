from unittest import TestCase

import json
import collections
from typing import NamedTuple
from niascape.utility.json import AsdictSupportJSONEncoder


class Asdict:
	# noinspection PyMethodMayBeStatic
	def _asdict(self):
		return {'name': 'asdict'}


class TestAsdictSupportJSONEncoder(TestCase):
	def test_encode(self):
		ret = json.dumps(None, cls=AsdictSupportJSONEncoder)
		self.assertEqual('null', ret)
		ret = json.dumps(True, cls=AsdictSupportJSONEncoder)
		self.assertEqual('true', ret)
		ret = json.dumps(False, cls=AsdictSupportJSONEncoder)
		self.assertEqual('false', ret)
		ret = json.dumps(1, cls=AsdictSupportJSONEncoder)
		self.assertEqual('1', ret)
		ret = json.dumps(1.1, cls=AsdictSupportJSONEncoder)
		self.assertEqual('1.1', ret)
		ret = json.dumps('hoge', cls=AsdictSupportJSONEncoder)
		self.assertEqual('"hoge"', ret)

	def test_encode_list(self):
		test = list()
		test.append('hoge')
		test.append(1)
		test.append(1.1)
		test.append([])
		test.append({})
		test.append(True)
		test.append(False)
		test.append(None)

		ret = json.dumps(test, cls=AsdictSupportJSONEncoder)
		self.assertEqual('["hoge", 1, 1.1, [], {}, true, false, null]', ret)

	def test_encode_dict(self):
		_dict = dict()
		_dict["str"] = 'hoge'
		_dict["int"] = 1
		_dict["float"] = 1.1
		_dict["list"] = []
		_dict["dict"] = {}
		_dict["true"] = True
		_dict["false"] = False
		_dict["none"] = None
		_dict[True] = "True"
		_dict[False] = "False"
		_dict[None] = "None"

		ret = json.dumps(_dict, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"str": "hoge", "int": 1, "float": 1.1, "list": [], "dict": {}, "true": true, "false": false, "none": null, "true": "True", "false": "False", "null": "None"}', ret)

		ret = json.dumps({1: 'int', 1.1: 'float'}, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"1": "int", "1.1": "float"}', ret)

	def test_encode_tuple(self):
		_tuple = ('hoge', 1)
		ret = json.dumps(_tuple, cls=AsdictSupportJSONEncoder)
		self.assertEqual('["hoge", 1]', ret)

		namedtuple = NamedTuple('namedtuple', (('key', str), ('val', int)))
		_namedtuple = namedtuple(*_tuple)
		ret = json.dumps(_namedtuple, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"key": "hoge", "val": 1}', ret)

		ret = json.dumps([_namedtuple], cls=AsdictSupportJSONEncoder)
		self.assertEqual('[{"key": "hoge", "val": 1}]', ret)

		namedtuple = collections.namedtuple('collections_namedtuple', ('key', 'val'))
		_namedtuple = namedtuple(*_tuple)
		ret = json.dumps(_namedtuple, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"key": "hoge", "val": 1}', ret)
		ret = json.dumps([_namedtuple], cls=AsdictSupportJSONEncoder)
		self.assertEqual('[{"key": "hoge", "val": 1}]', ret)

	def test_encode_class(self):
		o = Asdict()
		ret = json.dumps(o, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"name": "asdict"}', ret)
		ret = json.dumps([o], cls=AsdictSupportJSONEncoder)
		self.assertEqual('[{"name": "asdict"}]', ret)
		ret = json.dumps({'indict': o}, cls=AsdictSupportJSONEncoder)
		self.assertEqual('{"indict": {"name": "asdict"}}', ret)

	def test_encode_indent(self):
		ret = json.dumps([1, 2, 3], cls=AsdictSupportJSONEncoder, indent=4)
		self.assertEqual('[\n    1,\n    2,\n    3\n]', ret)
		ret = json.dumps([1, 2, 3], cls=AsdictSupportJSONEncoder, indent='  ')
		self.assertEqual('[\n  1,\n  2,\n  3\n]', ret)
		ret = json.dumps({'key': "val"}, cls=AsdictSupportJSONEncoder, indent='  ')
		self.assertEqual('{\n  "key": "val"\n}', ret)

	def test_encode_check_circular(self):
		ret = json.dumps('hoge', cls=AsdictSupportJSONEncoder)
		self.assertEqual('"hoge"', ret)
		ret = json.dumps('hoge', cls=AsdictSupportJSONEncoder, check_circular=False)
		self.assertEqual('"hoge"', ret)

	def test_encode_flort(self):
		ret = json.dumps([float("inf"), -float("inf"), float("inf") - float("inf")], cls=AsdictSupportJSONEncoder)
		self.assertEqual('[Infinity, -Infinity, NaN]', ret)
		with self.assertRaises(ValueError):
			json.dumps([float("inf"), -float("inf"), float("inf") - float("inf")], cls=AsdictSupportJSONEncoder, allow_nan=False)
