# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from consts import BornPositionList, BornYaw


class MatchStub(KBEngine.Entity):

	GAME_CAN_START_NUM = 2  # 一局游戏需要的玩家人数

	def __init__(self):
		KBEngine.Entity.__init__(self)
		KBEngine.globalData["MatchStub"] = self

		self.space_mgr = KBEngine.globalData['SpaceMgr']

		self._wait_match_set = set()  # 等待匹配的玩家列表

		INFO_MSG("[MatchStub], init match stub success.")

	def begin_match(self, entity_id):
		"""
		entity_id玩家开始进入匹配
		:param entity_id:
		:return:
		"""
		INFO_MSG("[MatchStub], entity_id:%s begin match." % entity_id)

		self._wait_match_set.add(entity_id)
		if len(self._wait_match_set) == MatchStub.GAME_CAN_START_NUM:
			self._match_success()
		else:
			self._notify_avatars_match_info()

	def _notify_avatars_match_info(self):
		"""
		通知匹配中的玩家匹配信息变化
		:return:
		"""
		cur_match_num = len(self._wait_match_set)
		for avatar_id in self._wait_match_set:
			avatar = KBEngine.entities.get(avatar_id, None)
			if not avatar:
				continue

			if not avatar.client:
				continue

			avatar.client.notify_match_info(cur_match_num)

	def _match_success(self):
		"""
		匹配成功的处理
		:return:
		"""
		self._notify_avatars_match_info()

		INFO_MSG("[MatchStub], match success.")

		avatar_info = dict()
		index = 0
		_readyAvatarSet = set()
		for _ava_id in self._wait_match_set:
			_avatar = KBEngine.entities.get(_ava_id, None)
			if not _avatar:
				continue

			_avatar.born_position = BornPositionList[index]
			_avatar.born_yaw = BornYaw[index]
			_readyAvatarSet.add(_avatar)
			index = index + 1  # noqa
			avatar_info[_avatar.id] = dict()
			avatar_info[_avatar.id]["born_position"] = _avatar.born_position
			avatar_info[_avatar.id]["born_yaw"] = _avatar.born_yaw

		self.space_mgr.enter_game_battle_space(_readyAvatarSet, avatar_info)

		# 匹配数据清空，完成一次匹配
		self._wait_match_set = set()
