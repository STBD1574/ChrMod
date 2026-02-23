# -*- coding: utf-8 -*-
from ChrMod.Module.ModuleManager import Module, ModuleType
import mod.client.extraClientApi as clientApi
import ChrMod.Api as Api

class HudTip(Module):
    def __init__(self):
        Module.__init__(self, "HudTip", "显示Hud提示（右上角的那个）。", ModuleType.VISUAL, True, None)
        Api.ListenForEvent("Minecraft", "Engine", "UiInitFinished", self, self.UiInitFinished, 10)
        self.mEnabled = False

    def OnEnable(self):
        self.mEnabled = True

    def OnDisable(self):
        self.mEnabled = False

    def UiInitFinished(self, args):
        screen = clientApi.GetTopUINode()
        def Update():
            if self.mEnabled:
                label = screen.GetBaseUIControl("variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/gamertag_label_for_splitscreen").asLabel()
                label.EnableTextShadow()
                label.SetText("§cC§eh§ar§bMod §7- §fV3 | Platform: " +  str(clientApi.GetPlatform()) + " | InputMode: " + str(clientApi.GetEngineCompFactory().CreatePlayerView("").GetToggleOption("INPUT_MODE") + 1) + " | FPS: " + str(int(clientApi.GetEngineCompFactory().CreateGame("").GetFps())))
        screen.Update = Update