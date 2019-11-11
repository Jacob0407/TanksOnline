# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
from IdManager import IDManager
from consts import MatchArgs, SpaceType, BornPositionList, BornYaw


class SpaceRoom(KBEngine.Space):
	def __init__(self):
		KBEngine.Space.__init__(self)

		self._wait_to_match_avatar_set = set()
		self._avatar_dict = {}  # 本space内所有的avatar列表
		self._waitToEnterList = list()  # 等待进入space的avatar

		self.spaceMgr = KBEngine.globalData['SpaceMgr']

	def enter(self, avatar_entity_call):
		if self.uType == SpaceType.SPACE_TYPE_HALL:
			avatar_entity_call.createCellEntity(self.cell)
		else:
			# 从大厅进入战场
			# 先从大厅离开
			avatar_entity_call.curHallSpace.leave(avatar_entity_call.id)
			avatar_entity_call.cell.onTeleportSpaceCB(self, self.cell, avatar_entity_call.born_position, (0, 0, 0))

		self._avatar_dict[avatar_entity_call.id] = avatar_entity_call

		avatar_entity_call.onEnterSpace(self.id, self.uType)

	def leave(self, avatar_id):
		avatar = self._avatar_dict.get(avatar_id, None)
		if avatar:
			del self._avatar_dict[avatar_id]

		self.cell and self.cell.leave(avatar_id)

	def onGetCell(self):
		DEBUG_MSG("[Space], onGetCell, id=%i, type=%i" % (self.id, self.uType))

		KBEngine.globalData["SpaceMgr"].onSpaceGetCell(self.id, self.uType, self)

		# 处理排队要进入本空间的列表
		for entityCall in self._waitToEnterList:
			self.enter(entityCall)
		# 清空
		self._waitToEnterList = []

	def onLoseCell(self):
		DEBUG_MSG("[Space], onLoseCell, id=%i, type=%i", (self.id, self.uType))

		KBEngine.globalData["SpaceMgr"].onSpaceLoseCell(self.id, self.uType)

	def addWaitToEnter(self, avatarEntityCall):
		"""
		当空间还没创建完毕时，把目标实体加入到等待进入房间的列表中
		:param avatarEntityCall: 要进入房间的目标实体
		:return:
		"""
		INFO_MSG("[SpaceRoom], %i, %i, avatar:%s addWaitToEnter." % (self.id, self.uType, avatarEntityCall))
		self._waitToEnterList.append(avatarEntityCall)

	def avatarReqMatch(self, avatarID):
		INFO_MSG("[SpaceRoom], %i, %i, avatar:%s reqMatch." % (self.id, self.uType, avatarID))

		self._wait_to_match_avatar_set.add(avatarID)

		matchNum = len(self._wait_to_match_avatar_set)
		if matchNum >= MatchArgs.BATTLE_ROOM_MATCH_PLAYER_NUM:
			INFO_MSG("[SpaceRoom], %i, %i, ready to enter battle room" % (self.id, self.uType))

			avatar_info = dict()
			index = 0
			_readyAvatarSet = set()
			for _ava_id in self._wait_to_match_avatar_set:
				_avatar = self._avatar_dict.get(_ava_id, None)
				if _avatar:
					_avatar.born_position = BornPositionList[index]
					_avatar.born_yaw = BornYaw[index]
					_readyAvatarSet.add(_avatar)
					index = index + 1  # noqa
					avatar_info[_avatar.id] = dict()
					avatar_info[_avatar.id]["born_position"] = _avatar.born_position
					avatar_info[_avatar.id]["born_yaw"] = _avatar.born_yaw

			self.spaceMgr.enterSpace(_readyAvatarSet, SpaceType.SPACE_TYPE_BATTLE, avatar_info)

			self._wait_to_match_avatar_set = set()
			return

		for ava_id in self._wait_to_match_avatar_set:
			_avatar = self._avatar_dict.get(ava_id, None)
			if not _avatar:
				continue

			_avatar.client.onMatch(matchNum)





