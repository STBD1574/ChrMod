# -*- coding: utf-8 -*-
# author Eison
# 2024/07/14

from .pyimport import Module
from .api import modapi, client, ui
from .api.platform import windows
from .module import manager
from .command import registry
from .ui import creator
from . import modlog, patch

sys     = Module('sys')
QSecImp = Module('QSecImp')


class EventHandler:
    def create(self):
        modapi.ListenForEngineClient('ClickChatSendClientEvent', self, self.ClickChatSendClientEvent, 10)
        modapi.ListenForEngineClient('UnLoadClientAddonScriptsBefore', self, self.UnLoadClientAddonScriptsBefore, 10)
        modapi.ListenForEngineClient('UiInitFinished', self, self.UiInitFinished, 10)
        modapi.ListenForEngineClient('ScreenSizeChangedClientEvent', self, self.ScreenSizeChangedClientEvent, 10)
        modapi.ListenForEngineClient('OnKeyPressInGame', self, self.OnKeyPressInGame, 10)

    def destroy(self):
        ''' 不知道为什么，它需要手动销毁 '''
        modapi.UnListenForEngineClient('ClickChatSendClientEvent', self, self.ClickChatSendClientEvent, 10)
        modapi.UnListenForEngineClient('UnLoadClientAddonScriptsBefore', self, self.UnLoadClientAddonScriptsBefore, 10)
        modapi.UnListenForEngineClient('UiInitFinished', self, self.UiInitFinished, 10)
        modapi.UnListenForEngineClient('ScreenSizeChangedClientEvent', self, self.ScreenSizeChangedClientEvent, 10)
        modapi.UnListenForEngineClient('OnKeyPressInGame', self, self.OnKeyPressInGame, 10)

    def ClickChatSendClientEvent(self, args): # type: (dict[str, str]) -> None
        if not args['message'].startswith(registry.GetRegistry().prefix):
            args['cancel'] = False
            return
        
        args['cancel'] = True
        message = args['message'].lstrip(registry.GetRegistry().prefix)

        try:
            registry.GetRegistry().Execute(message)
        except Exception:
            client.DisplayClientMessage("§cC§eh§ar§bMod §7>§r Unknown command: '{}', plaese type {}help for help.".format(message, registry.GetRegistry().prefix))

    def UnLoadClientAddonScriptsBefore(self, args):
        patch.reset()
        modlog.destroy()
        self.destroy()

    def UiInitFinished(self, args):
        package = sys.modules[__name__].__package__

        creator.Screen('chrmod', 'ClickGUI', package + '.ui.clickgui.ClickGUI')
        creator.Screen('chrmod', 'HudGUI', package + '.ui.hudgui.HudGUI')

        ui.CreateUI('chrmod', 'HudGUI', { })

    def ScreenSizeChangedClientEvent(self, args):
        # windows.SetWindowTitle(QSecImp.qsecmgr, windows.GetWindowHandle(QSecImp.qsecmgr), '({}, {}) ChrMod | Login as {}'.format(int(args['afterX']), int(args['afterY']), '中文名测试'))
        pass

    def OnKeyPressInGame(self, args):
        if args['screenName'] != 'hud_screen' or args['isDown'] != '1':
            if args['key'] == '27':
                ui.PopTopUI()
            return
        
        for module in manager.GetManager().modules.itervalues():
            if str(module.key) == args['key']:
                module.SetEnabled(not module.enabled)
                break

eventHandler = EventHandler()

def GetEventHandler(): # type: () -> EventHandler
    return eventHandler