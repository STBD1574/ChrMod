# -*- coding: utf-8 -*-
# author Eison
# 2024/08/01

from mod.client.ui.screenNode import ScreenNode
from ..api import client, modapi, ui
from . import creator

class HudGUI(ScreenNode):
	def __init__(self, namespace, name, param):
		ScreenNode.__init__(self, namespace, name, param)

		self.chrmod_tip = None

	def Create(self):
		chrmod_tip_bg = creator.Image(self, 'chrmod_tip_bg', None, False)
		creator.SetAnchor(chrmod_tip_bg, 'top_right')
		
		self.chrmod_tip = creator.Label(self, 'chrmod_tip', chrmod_tip_bg, False)
		self.chrmod_tip.EnableTextShadow()

		self.chrmod_tip.SetPosition((-16, 16))	


		self.UpdateScreen(True)

	def SetTip(self, tip, sync):
		if self.chrmod_tip:
			self.chrmod_tip.SetText(tip, sync)

	def Update(self):
		pass