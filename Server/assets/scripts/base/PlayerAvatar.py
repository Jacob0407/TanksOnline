# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class PlayerAvatar(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		self.hallSpaceID = 0  # 所在的大厅spaceid
		self.battleSpaceID = 0  # 所在的战场spaceid
		self.born_position = None  # 出生的坐标
		self.born_yaw = 0  # 出生时的yaw值

		self.space_mgr = KBEngine.globalData["SpaceMgr"]

		INFO_MSG("[PlayerAvatar], init success.")

	def ready_enter_game_hall(self):
		"""
		准备进入游戏大厅，只在第一次连接游戏时调用
		:return:
		"""
		game_hall_cell = self.space_mgr.game_hall.cell
		self.createCellEntity(game_hall_cell)

	def onClientEnabled(self):
		INFO_MSG("[PlayerAvatar], onClientEnabled, ready to enter game hall")

	def onGetCell(self):
		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG('PlayerAvatar::onGetCell: %s' % self.cell)
		# 真正进入大厅
		self.space_mgr.enter_game_hall(self)

	def destroySelf(self):
		"""
		"""
		DEBUG_MSG("PlayerAvatar::destroySelf: %s" % self.cell)

	def onEnterSpace(self, _spaceID):
		INFO_MSG("[PlayerAvatar], %s, enter space:%s" % (self, _spaceID))

	def reqMatch(self):
		INFO_MSG("[PlayerAvatar], %s, reqMatch" % (self.id))

		match_stub = KBEngine.globalData["MatchStub"]
		match_stub and match_stub.begin_match(self.id)

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



