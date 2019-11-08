# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from IdManager import IDManager
from consts import SpaceType


class PlayerAvatar(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		self.hallSpaceID = 0  # 所在的大厅spaceid
		self.battleSpaceID = 0  # 所在的战场spaceid
		self.born_position = None  # 出生的坐标
		self.born_yaw = 0  # 出生时的yaw值
		WARNING_MSG("PlayerAvatar::base::init")

	@property
	def curHallSpace(self):
		return KBEngine.entities.get(self.hallSpaceID, None) if self.hallSpaceID else None

	def onClientEnabled(self):
		INFO_MSG("PlayerAvatar::onClientEnabled, ready to enter space")
		spaceMgr = KBEngine.globalData['SpaceMgr']
		spaceMgr and spaceMgr.enterSpace({self}, SpaceType.SPACE_TYPE_HALL)

	def onGetCell(self):
		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG('PlayerAvatar::onGetCell: %s' % self.cell)

	def destroySelf(self):
		"""
		"""
		DEBUG_MSG("PlayerAvatar::destroySelf: %s" % self.cell)

	def onEnterSpace(self, _spaceID, _spaceType):
		if _spaceType == SpaceType.SPACE_TYPE_HALL:
			self.hallSpaceID = _spaceID
		elif _spaceType == SpaceType.SPACE_TYPE_BATTLE:
			self.battleSpaceID = _spaceID

		INFO_MSG("[PlayerAvatar], %s, enter space:%s.%s" % (self, _spaceID, _spaceType))

	def reqMatch(self):
		INFO_MSG("[PlayerAvatar], %s, reqMatch" % (self.id))
		self.curHallSpace and self.curHallSpace.avatarReqMatch(self.id)

	# --------------------------------------------------------------------------------------------
	#                              Callbacks
	# --------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))

	def onClientDeath(self):
		"""
		KBEngine method.
		entity丢失了客户端实体
		"""
		DEBUG_MSG("Avatar[%i].onClientDeath:" % self.id)

	def onClientGetCell(self):
		"""
		KBEngine method.
		客户端已经获得了cell部分实体的相关数据
		"""
		INFO_MSG("Avatar[%i].onClientGetCell:%s" % (self.id, self.client))

	def onDestroyTimer(self):
		DEBUG_MSG("Avatar::onDestroyTimer: %i" % (self.id))
		self.destroySelf()

	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)



