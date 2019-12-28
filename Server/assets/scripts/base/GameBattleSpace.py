# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from consts import SpaceType


class GameBattleSpace(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

		self.space_mgr = KBEngine.globalData["SpaceMgr"]
		self._avatar_set = set()  # 本space内所有的avatar集合
		self._wait_to_enter_set = set()  # 等待进入space的avatar

	def enter(self, avatar_entity_call):
		INFO_MSG("[GameBattleSpace], id=%i, entity:%s enter space." % (self.id, avatar_entity_call))

		avatar_entity_call.cell.teleport_space(self.cell, avatar_entity_call.born_position, (0, 0, 0))
		self._avatar_set.add(avatar_entity_call.id)

		avatar_entity_call.on_enter_space(self.id)

	def leave(self, avatar_id):
		avatar = self._avatar_dict.get(avatar_id, None)
		if avatar:
			del self._avatar_dict[avatar_id]

		self.cell and self.cell.leave(avatar_id)

	def add_entity_to_wait_list(self, entity_id):
		"""
		当空间还没创建完毕时，把目标实体加入到等待进入房间的列表中
		:param entity_id:
		:return:
		"""
		INFO_MSG("[GameBattleSpace], %i, avatar:%s add to wait list." % (self.id, entity_id))
		self._wait_to_enter_set.add(entity_id)

	def onGetCell(self):
		INFO_MSG("[GameBattleSpace], onGetCell, id=%i" % self.id)

		self.space_mgr.on_space_get_cell(SpaceType.SPACE_TYPE_BATTLE, self.id)

		# 处理排队要进入本空间的列表
		for entity_id in self._wait_to_enter_set:
			entity = KBEngine.entities.get(entity_id, None)
			entity and self.enter(entity)

		# 清空
		self._wait_to_enter_set = set()

	def onLoseCell(self):
		DEBUG_MSG("[GameBattleSpace], onLoseCell, id=%i", self.id)
