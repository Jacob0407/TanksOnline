# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class SpaceMgr(KBEngine.Entity):

	def __init__(self):
		KBEngine.Entity.__init__(self)

		self._spaceUtypeDict = {}
		self._spaces = {}

		KBEngine.globalData["SpaceMgr"] = self

	def enterSpace(self, avatarEntityCall, spaceUtype):
		"""
		:param avatarEntityCall: 玩家的entitycall
		:param spaceUtype: 请求进入的空间类型
		:return:
		"""

		space = self._spaceUtypeDict.get(spaceUtype, None)
		if not space:
			INFO_MSG("[Space], avatar:%s enter space error, space_type:%i " % (avatarEntityCall, spaceUtype))

			new_space = KBEngine.createEntityLocally("SpaceRoom", {'uType': spaceUtype})  # 创建大厅
			new_space and new_space.addWaitToEnter(avatarEntityCall)

			return

		space.enter(avatarEntityCall)

	def leaveSpace(self, avatarId, spaceKey):
		"""
		:param avatarId: 用户id
		:param spaceKey: 空间id
		:return:
		"""
		space = self._spaces.get(spaceKey, None)
		if not space:
			ERROR_MSG("[Space], leaveSpace error, key:%s" % (spaceKey))
			return

		space.leave(avatarId)

	def onSpaceGetCell(self, key, spaceUtype, spaceEntityCall):
		"""
		space在cell上成功创建后
		:param key:
		:param spaceUtype:
		:param spaceEntityCall:
		:return:
		"""

		DEBUG_MSG("[Space], onSpaceGetCell, key:%s, type:%s, call:%s" % (key, spaceUtype, spaceEntityCall))
		self._spaceUtypeDict[spaceUtype] = spaceEntityCall
		self._spaces[key] = spaceEntityCall

	def onSpaceLoseCell(self, key, uType):
		DEBUG_MSG("[Space], onSpaceLoseCell, key:%s, type:%s" % (key, type))

		del self._spaceUtypeDict[uType]
		del self._spaces[key]
