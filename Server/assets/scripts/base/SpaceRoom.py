# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from IdManager import IDManager


class SpaceRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)
		room_id = IDManager.generate_room_id()
		INFO_MSG("init space room, id:%s" % room_id)
		KBEngine.globalData[room_id] = self
