# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.active_avatar = None
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("account[%i] entities enable. entityCall:%s" % (self.id, self.client))

		# 原账号在线
		if self.active_avatar:
			if self.active_avatar.reconnect_flag:
				INFO_MSG("[Account], %i re login avatar battle space id:%s" % (self.id, self.active_avatar.battle_space_id))
				self.giveClientTo(self.active_avatar)
				self.active_avatar.re_connect_to_battle_space()
			return

		self.become_player_avatar()
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里reloginBaseapp
		"""
		INFO_MSG("[Account], %i onLogOnAttempt: ip=%s, port=%i, selfclient=%s, %s" % (self.id, ip, port, self.client, self.active_avatar))

		# 置空掉之前avatar的client
		if self.active_avatar:
			self.active_avatar.giveClientTo(self)
			self.active_avatar.reconnect_flag = True

		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		if self.active_avatar:
			self.active_avatar.account_entity = None
			self.active_avatar = None

		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()

	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("[Account], %i, onDestroy" % self.id)

		if self.active_avatar:
			self.active_avatar.account_entity = None

			try:
				self.active_avatar.destroy_self()
			except:
				pass

			self.active_avatar = None

	def become_player_avatar(self):
		"""
		从Account成为Avatar
		:return:
		"""

		avatar = KBEngine.createEntityLocally("PlayerAvatar", {})
		if avatar:
			DEBUG_MSG("[Account], %i, become_player_avatar\n" % self.id)
			avatar.account_entity = self
			self.active_avatar = avatar
			self.giveClientTo(self.active_avatar)

			avatar.ready_enter_game_hall()

