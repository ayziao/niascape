from typing import Union, Callable
from importlib import import_module

import logging

logger = logging.getLogger(__name__)


def dynamic_get_method(module_name: str, method_name: str) -> Union[Callable, None]:
	actions = method_name.rsplit('.', 1)
	if len(actions) > 1:
		module_name += '.' + actions[0]
		method_name = actions[1]

	module = import_module(module_name)

	try:
		method = getattr(module, method_name)
		if not callable(method):
			method = None
	except AttributeError:
		logger.debug("AttributeError: %s", method_name)
		method = None

	return method


class Setting:
	def __init__(self):
		self.ini = None

	def _load_setting(self):
		pass

	def get_setting(self):
		pass

# TODO コンフィグパーサの使いづらいところどうにかする
