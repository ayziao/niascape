import logging

logger = logging.getLogger(__name__)


class Setting:
	def __init__(self):
		self.ini = None

	def _load_setting(self):
		pass

	def get_setting(self):
		pass

# TODO コンフィグパーサの使いづらいところどうにかする
