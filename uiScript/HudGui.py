# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import ChrMod.Api as Api
import ChrMod.Module.ModuleManager as ModuleManager
from ChrMod.uiScript.Gui import ControlCreator, GuiTools

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

class Main(ScreenNode):
	def __init__(self, namespace, name, param):
		ScreenNode.__init__(self, namespace, name, param)

	def Create(self):
		print(" ==== ChrMod TouchGui Create ====")
		self.button = ControlCreator.Button(self, "button_clickgui", self.GetBaseUIControl("/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"), True)
		self.button.SetSize((32, 24), True)
		self.button.AddTouchEventParams({"isSwallow":True})
		self.button.SetButtonTouchDownCallback(lambda args : ModuleManager.GetModule("ClickGui").OnEnable())
		map(lambda x : self.button.SetFullPosition(x[0], {"followType": "parent", "relativeValue": x[1]}), [("x", -0.45), ("y", -0.4)])
		button_image = ControlCreator.Image(self, "default", self.button, False)
		button_image.SetSprite("textures/ui/Black.png")
		button_image.SetAlpha(0.5)
		button_image.SetImageAdaptionType("originNineSlice", (0, 0, 0, 0))
		GuiTools.SetFullSize(button_image)
		button_text = ControlCreator.Label(self, "button_text", self.button, False)
		button_text.SetText("ClickGUI")
		button_text.SetLayer(10, True, False)
		self.UpdateScreen(True)

	def Destroy(self):
		print(" ==== ChrMod TouchGui Destroy ====")
	
	def Update(self):
		inputMode = Api.GetInputMode() == 1
		if self.button.GetVisible() != inputMode:
			self.button.SetVisible(inputMode, True)
