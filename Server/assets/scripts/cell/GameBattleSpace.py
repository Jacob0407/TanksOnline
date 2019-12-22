# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from AVATAR_INFO import TAvatarInfoList, TAvatarInfo


class GameBattleSpace(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

		self._avatar_set = set()

		INFO_MSG("[GameBattleSpace], %s init game battle space succ." % self.id)

	def enter(self, entity):
		INFO_MSG("[GameBattleSpace], %s , entity: %s enter space." % (self.id, entity))

		self._avatar_set.add(entity.id)
		entity.client.enterBattleSpace(self.get_all_avatar_info())

	def leave(self, entityID):
		"""
		defined method.
		离开场景
		"""
		DEBUG_MSG('Space::onLeave space entityID = %i.' % (entityID))

	def get_all_avatar_info(self):
		"""
		获得房间内所有玩家的信息
		:return: dict()
		"""

		DEBUG_MSG("Space::Room get_all_avatar_info, info:%s" % (self.avatar_info))

		avatar_info_list = TAvatarInfoList()
		for entity_id, data in self.avatar_info.items():
			avatar_info = TAvatarInfo()
			avatar_info.extend([entity_id, data["born_position"], data["born_yaw"]])
			avatar_info_list[entity_id] = avatar_info

		return avatar_info_list


