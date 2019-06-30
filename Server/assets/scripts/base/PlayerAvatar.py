# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from IdManager import IDManager


class PlayerAvatar(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		WARNING_MSG("PlayerAvatar::base::init")

	def onClientEnabled(self):
		WARNING_MSG("PlayerAvatar::onClientEnabled")
		space_room = KBEngine.globalData[IDManager.get_cur_room_id()]
		self.createCellEntity(space_room.cell)
