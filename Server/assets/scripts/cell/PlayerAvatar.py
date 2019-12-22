# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class PlayerAvatar(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)

		INFO_MSG("[PlayerAvatar], init success. %i" % self.id)
		self.client.onEnter()

	def teleport_space(self, space_cell_entity_call, position, direction):
		INFO_MSG("[PlayerAvatar], id = %i , base req cell to teleport space, %s" % (self.id, space_cell_entity_call))

		self.teleport(space_cell_entity_call, position, direction)

	def onTeleportSuccess(self, space_room):
		"""
		KBEngine method.
		"""
		INFO_MSG("[PlayerAvatar], id = %i, space_id:%s, onTeleportSuccess: %s, id:%s" % (self.id, self.spaceID, space_room, space_room.id))

		space_room.enter(self)
