# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class GameHall(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

		INFO_MSG("[GameHall], %s init game GameHall space succ." % self.id)

	def enter(self, entity):
		INFO_MSG("[GameHall], %s , entity: %s enter space." % (self.id, entity))

	def leave(self, entity_id):
		"""
		defined method.
		离开场景
		"""
		DEBUG_MSG('[GameHall], onLeave space entity_id = %i.' % entity_id)