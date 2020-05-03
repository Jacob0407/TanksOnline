# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class PlayerAvatar(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Entity.__init__(self)

		self.account_entity = None  # 对应的account
		self.battle_space_id = 0  # 所在的战场spaceid
		self.born_position = None  # 出生的坐标
		self.born_yaw = 0  # 出生时的yaw值

		self.need_destroy = False
		self.reconnect_flag = False

		self.space_mgr = KBEngine.globalData["SpaceMgr"]

		INFO_MSG("[PlayerAvatar], init success.")

	def ready_enter_game_hall(self):
		"""
		准备进入游戏大厅，只在第一次连接游戏时调用
		:return:
		"""
		game_hall_cell = self.space_mgr.game_hall.cell
		self.createCellEntity(game_hall_cell)

	def back_to_game_hall(self):
		"""
		从其他服返回到大厅
		:return:
		"""
		self.space_mgr.leaveSpace(self.id, self.battle_space_id)
		self.space_mgr.enter_game_hall(self)

	def onClientEnabled(self):
		INFO_MSG("[PlayerAvatar], onClientEnabled, ready to enter game hall")

	def onGetCell(self):
		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG("[PlayerAvatar], %s, %i, onGetCell" % (self, self.id))
		# 真正进入大厅
		self.space_mgr.enter_game_hall(self)

	def onLoseCell(self):
		# 销毁base
		if self.need_destroy and not self.isDestroyed:
			INFO_MSG("[PlayerAvatar], %s, %i, on lose cell." % (self, self.id))
			self.destroy(False, True)

	def after_account_re_login(self, battle_space_id, born_pos):
		self.battle_space_id = battle_space_id
		self.born_position = born_pos

	def re_connect_to_battle_space(self):
		if self.battle_space_id > 0:
			_battle_space = KBEngine.entities.get(self.battle_space_id, None)
			_battle_space_cell = _battle_space.cell
			if _battle_space and _battle_space_cell:
				INFO_MSG("[PlayerAvatar], %s, %i, re_connect_to_battle_space" % (self, self.id))
				self.cell.teleport_space(_battle_space_cell, self.born_position, (0, 0, 0))

	def destroy_self(self, destroy_account=False):
		"""
		"""
		DEBUG_MSG("[PlayerAvatar], %s, %i, destroy_self" % (self, self.id))

		if self.cell is not None:
			# 销毁cell实体
			self.destroyCellEntity()

		# 如果帐号ENTITY存在 则也通知销毁它
		destroy_account and self.account_entity and self.account_entity.destroy()

		self.need_destroy = True

	def on_enter_space(self, _space_id):
		if self.space_mgr.game_hall.id == _space_id:
			return

		INFO_MSG("[PlayerAvatar], %s, %i, enter space:%s" % (self, self.id, _space_id))
		self.battle_space_id = _space_id

	def reqMatch(self):
		INFO_MSG("[PlayerAvatar], %s, %i, reqMatch" % (self, self.id))

		if self.battle_space_id > 0:
			INFO_MSG("[PlayerAvatar], %s, %i, already in battle space:%d, can't req match" % (self, self.id, self.battle_space_id))
			return

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
		DEBUG_MSG("[PlayerAvatar], %s, %i onClientDeath:" % (self, self.id))

	def onClientGetCell(self):
		"""
		KBEngine method.
		客户端已经获得了cell部分实体的相关数据
		"""
		INFO_MSG("[PlayerAvatar], %s, %i, onClientGetCell" % (self, self.id))

	def onDestroyTimer(self):
		DEBUG_MSG("[PlayerAvatar], %s, %i, onDestroyTimer" % (self, self.id))
		self.destroy_self()

	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("[PlayerAvatar], %s, %i, onDestroy" % (self, self.id))

		if self.account_entity != None:
			self.account_entity.active_avatar = None
			self.account_entity = None



