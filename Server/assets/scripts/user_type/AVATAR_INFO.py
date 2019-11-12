# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TAvatarInfo(list):
	"""
	"""

	def __init__(self):
		"""
		"""
		list.__init__(self)

	def asDict(self):
		data = {
			"entity_id"		: self[0],
			"born_position"	: self[1],
			"born_yaw"		: self[2],
		}

		return data

	def createFromDict(self, dictData):
		self.extend([dictData["entity_id"], dictData["born_position"], dictData["born_yaw"]])
		return self


class AVATAR_INFO_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TAvatarInfo().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TAvatarInfo)


avatar_info_inst = AVATAR_INFO_PICKLER()


class TAvatarInfoList(dict):
	"""
	"""

	def __init__(self):
		"""
		"""
		dict.__init__(self)

	def asDict(self):
		datas = []
		dct = {"values": datas}

		for key, val in self.items():
			datas.append(val)

		return dct

	def createFromDict(self, dictData):
		for data in dictData["values"]:
			self[data[0]] = data
		return self


class AVATAR_INFO_LIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TAvatarInfoList().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TAvatarInfoList)


avatar_info_list_inst = AVATAR_INFO_LIST_PICKLER()


