"""
niascape.entity.basedata

ベースデータエンティティ
"""
# from typing import NamedTuple
from datetime import datetime


class Basedata:
	# FUTURE pypyが3.6互換になったら
	# class Basedata(NamedTuple):
	# identifier: str
	# title: str
	# tags: str
	# body: str
	# datetime: datetime
	# utctime: datetime

	def __init__(self, identifier: str, title: str, tags: str, body: str, datetime_: datetime) -> None:
		self.identifier = identifier
		self.title = title
		self.tags = tags
		self.body = body
		self.datetime = datetime_
		# self.utctime = utctime
		pass

	def _asdict(self):
		return self.__dict__
