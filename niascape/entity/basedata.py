"""
niascape.entity.basedata

ベースデータエンティティ
"""
# from typing import NamedTuple
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)


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
		if type(datetime_) is datetime:
			self.datetime = datetime_
			self.utctime = datetime_ - timedelta(hours=9)
		else:
			self.datetime = datetime.strptime(datetime_[0:19], '%Y-%m-%d %H:%M:%S')  # PENDING ミリ秒の塩梅をどうするか
			self.utctime = self.datetime - timedelta(hours=9)

		logger.log(5, self.__dict__)

	def _asdict(self):
		return self.__dict__
