# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from consts import SpaceType


class SpaceMgr(KBEngine.Entity):

	def __init__(self):
		KBEngine.Entity.__init__(self)

		self._spaces = {}  # space_type: [space_id]

		KBEngine.globalData["SpaceMgr"] = self

		self._game_hall = None

	@property
	def game_hall(self):
		if self._game_hall:
			return self._game_hall

		space_id_list = self._spaces.get(SpaceType.SPACE_TYPE_HALL, list())
		if space_id_list is None:
			return None

		self._game_hall = KBEngine.entities.get(space_id_list[0], None)

		return self._game_hall

	def enter_game_hall(self, entity_call):
		"""
		进入游戏大厅
		:param entity_call:
		:return:
		"""
		if self.game_hall is None:
			ERROR_MSG("[SpaceMgr], game hall is None")
			return

		INFO_MSG("[SpaceMgr], %s ready enter game hall:%s" % (entity_call, self.game_hall))
		self.game_hall.enter(entity_call)

	def enter_game_battle_space(self, entity_call_set, avatar_info):
		"""
		一群玩家进入游戏战场
		:param entity_call_set:
		:param avatar_info:
		:return:
		"""
		battle_space = KBEngine.createEntityLocally("GameBattleSpace", {'avatar_info': avatar_info})
		if not battle_space:
			return

		for entity_call in entity_call_set:
			battle_space.add_entity_to_wait_list(entity_call.id)

	def leaveSpace(self, avatarId, spaceKey):
		"""
		:param avatarId: 用户id
		:param spaceKey: 空间id
		:return:
		"""
		space = self._spaces.get(spaceKey, None)
		if not space:
			ERROR_MSG("[Space], leaveSpace error, key:%s" % (spaceKey))
			return

		space.leave(avatarId)

	def on_space_get_cell(self, space_type, space_entity_id):
		"""
		space在cell上成功创建后进行注册
		:param space_type:
		:param space_entity_id:
		:return:
		"""
		if space_type not in self._spaces:
			self._spaces[space_type] = list()

		self._spaces[space_type].append(space_entity_id)

	def on_space_lose_cell(self, key, uType):
		pass
