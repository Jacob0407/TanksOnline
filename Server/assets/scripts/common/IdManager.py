# -*- coding: utf-8 -*-

"""
	ID生成器
"""


class IDManager:
	_room_id = 0

	def __init__(self):
		pass

	@staticmethod
	def generate_room_id():
		IDManager._room_id += 1
		return "room_%d" % IDManager._room_id

	@staticmethod
	def get_cur_room_id():
		return "room_%d" % IDManager._room_id
