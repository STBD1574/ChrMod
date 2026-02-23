# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import ChrMod.Module.ModuleManager as ModuleManager
import ChrMod.Api as Api
from ChrMod.uiScript.Gui import ControlCreator, GuiTools, ButtonUIControl, ImageUIControl, LabelUIControl

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

class Main(ScreenNode):
	def __init__(self, namespace, name, param):
		ScreenNode.__init__(self, namespace, name, param)
		self.args = param
		self.moveCotrol, self.moveX, self.moveY = None, 0.0, 0.0

	def Create(self):
		print(" ==== ChrMod ClickGui Create ====")
		clientApi.GetEngineCompFactory().CreatePostProcess("").SetEnableGaussianBlur(True)
		# clickgui background
		self.background = ControlCreator.Image(self, "background", self.GetBaseUIControl("/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"), False)
		self.background.SetSprite(self.args["background"]) #未来版本添加，自定义图片
		self.background.SetAlpha(0.2)
		self.background.SetImageAdaptionType("originNineSlice", (0, 0, 0, 0))
		GuiTools.SetFullSize(self.background)
		# clickgui closeButton
		self.closeButton = ControlCreator.Button(self, "close_button", self.background, False)
		closeImage = ControlCreator.Image(self, "default", self.closeButton, False)
		closeImage.SetSprite("textures/ui/close_button_default_light.png")
		self.closeButton.AddTouchEventParams({"isSwallow":True})
		self.closeButton.SetButtonTouchDownCallback(lambda args : self.CloseButtonClick())
		self.closeButton.SetSize((16, 16), True)
		map(lambda x : x("top_right"), [self.closeButton.SetAnchorFrom, self.closeButton.SetAnchorTo])
		GuiTools.SetFullSize(closeImage)
		# clickgui modules
		self.CreateType()
		# clickgui user info
		userInfo = ControlCreator.Label(self, "user_info", self.background, False)
		map(lambda x : x("bottom_right"), [userInfo.SetAnchorFrom, userInfo.SetAnchorTo])
		userInfo.SetText("ChrMod | Login as " + Api.Entity.GetName(clientApi.GetLocalPlayerId()), False)
		# update screen
		self.UpdateScreen(False)

	def CreateType(self):
		def Coroutine():
			def CreateButton(scroll, name, alpha, text): #type: (any, str, float, str) -> tuple[ButtonUIControl, ImageUIControl, LabelUIControl]
				button = ControlCreator.Button(self, name, scroll, False)
				button.AddTouchEventParams({"isSwallow":True})
				button.AddHoverEventParams()
				image = ControlCreator.Image(self, "image", button, False)
				image.SetSprite("textures/ui/white_background.png")
				image.SetImageAdaptionType("originNineSlice", (0, 0, 0, 0))
				image.SetAlpha(alpha)
				GuiTools.SetFullSize(image)
				label = ControlCreator.Label(self, "text", image, False)
				label.SetText(text)
				return button, image, label
			spawn = 0
			for moduleType, modules in ModuleManager.GetModuleTypes().items():
				scroll = ControlCreator.StackPanel(self, "type_" + moduleType, self.background, False)
				scroll.SetOrientation("vertical")
				scroll.SetPosition((spawn, 0))
				scroll.SetSize((64, 16), True)
				# type name
				button, image, label = CreateButton(scroll, "name_button", 0.6, moduleType)
				# type modules
				def ModuleButton(module): #type: (ModuleManager.Module) -> None
					moduleButton, moduleImage, moduleLabel = CreateButton(scroll, "module_" + module.name, 0.5 if module.open else 0.4, module.name)
					moduleButton.SetButtonHoverInCallback(lambda args : moduleImage.SetAlpha(0.6))
					moduleButton.SetButtonHoverOutCallback(lambda args : moduleImage.SetAlpha(0.5 if module.open else 0.4))
					moduleButton.SetButtonTouchDownCallback(lambda args : ModuleManager.ChangeModuleState(module, not module.open, { }, False))				
				for module in modules:
					ModuleButton(module)
					yield
				# next
				spawn += 64
			self.UpdateScreen(True)
		clientApi.StartCoroutine(Coroutine)

	def Destroy(self):
		print(" ==== ChrMod ClickGui Destroy ====")
		self.args["module"].open = False
		clientApi.GetEngineCompFactory().CreatePostProcess("").SetEnableGaussianBlur(False)
		pass

	def Update(self):
		pass

	def CloseButtonClick(self):
		clientApi.PopTopUI()