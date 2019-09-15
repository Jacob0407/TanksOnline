# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *


class PlayerAvatar(KBEngine.Entity):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		WARNING_MSG("PlayerAvatar::cell::init")
		self.client.onEnter()

