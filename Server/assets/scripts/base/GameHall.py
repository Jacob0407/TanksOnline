# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from consts import SpaceType


class GameHall(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

		self.space_mgr = KBEngine.globalData["SpaceMgr"]
		self._avatar_set = set()  # 本space内所有的avatar集合

	def enter(self, avatar_entity_call):
		INFO_MSG("[GameHall], id=%i, entity:%s enter space." % (self.id, avatar_entity_call))

		self._avatar_set.add(avatar_entity_call.id)

		avatar_entity_call.on_enter_space(self.id)

	def leave(self, avatar_id):
		avatar = self._avatar_dict.get(avatar_id, None)
		if avatar:
			del self._avatar_dict[avatar_id]

		self.cell and self.cell.leave(avatar_id)

	def onGetCell(self):
		INFO_MSG("[GameHall], onGetCell, id=%i" % self.id)

		self.space_mgr.on_space_get_cell(SpaceType.SPACE_TYPE_HALL, self.id)

	def onLoseCell(self):
		DEBUG_MSG("[GameHall], onLoseCell, id=%i", self.id)





