# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from AVATAR_INFO import TAvatarInfoList


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

	def onTeleportSuccess(self, space_room):
		"""
		KBEngine method.
		"""
		DEBUG_MSG("PlayerAvatar::onTeleportSuccess: %s, %s" % (space_room, space_room.get_all_avatar_info()))

		space_room.on_enter(self)




