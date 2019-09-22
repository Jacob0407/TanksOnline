# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class SpaceRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

	def leave(self, entityID):
		"""
		defined method.
		离开场景
		"""
		DEBUG_MSG('Space::onLeave space entityID = %i.' % (entityID))


