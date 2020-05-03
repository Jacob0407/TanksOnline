# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from AVATAR_INFO import TAvatarInfoList, TAvatarInfo


class GameBattleSpace(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

		self._avatar_set = set()

		INFO_MSG("[GameBattleSpace], %s init game battle space succ." % self.id)

	def enter(self, entity):
		INFO_MSG("[GameBattleSpace], %s , entity: %s enter space." % (self.id, entity))

		self._avatar_set.add(entity.id)
		entity.client.enterBattleSpace()

	def leave(self, entityID):
		"""
		defined method.
		离开场景
		"""
		DEBUG_MSG('Space::onLeave space entityID = %i.' % (entityID))


	def end_game(self):
		"""
		结束游戏
		:return:
		"""
		for _avatar_id in self._avatar_set:
			_avatar = KBEngine.entities.get(_avatar_id, None)
			_avatar and _avatar.base.back_to_game_hall()

