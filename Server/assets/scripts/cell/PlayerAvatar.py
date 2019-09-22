# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class PlayerAvatar(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		WARNING_MSG("PlayerAvatar::cell::init")
		self.client.onEnter()

		self.curSpaceBaseEntityCall = None

	def onTeleportSpaceCB(self, spaceBaseEntityCall, spaceCellEntityCall, position, direction):
		"""
		defined.
		baseapp返回teleportSpace的回调
		"""
		DEBUG_MSG("PlayerAvatar::onTeleportSpaceCB. spaceBase:%s...spaceCell:%s" % (spaceBaseEntityCall, spaceCellEntityCall))

		self.curSpaceBaseEntityCall = spaceBaseEntityCall
		self.teleport(spaceCellEntityCall, position, direction)

	def onTeleportSuccess(self, nearbyEntity):
		"""
		KBEngine method.
		"""
		DEBUG_MSG("PlayerAvatar::onTeleportSuccess: %s" % (nearbyEntity))
		self.client.onEnterBattleRoom()


