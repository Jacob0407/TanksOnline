# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from AVATAR_INFO import TAvatarInfoList, TAvatarInfo


class SpaceRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)
		DEBUG_MSG('SpaceRoom::init, room_type= %i, avatar_info:%s ' % (self.room_type, self.avatar_info))
		self._all_avatar_entity = {}

	def on_enter(self, entity):
		DEBUG_MSG("SpaceRoom::on_enter")
		self._all_avatar_entity[entity.id] = entity
		if len(self._all_avatar_entity) < len(self.avatar_info):
			return

		for _, entity in self._all_avatar_entity.items():
			entity.client.onEnterBattleRoom(self.get_all_avatar_info())

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


