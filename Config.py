# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import json
import os
import ChrMod.Module.ModuleManager as ModuleManager
import ChrMod.Command.Commands.Platform as Platform
import ChrMod.Command.Commands.InputMode as InputMode
import Client
import Api

def LoadConfig(fileName): #type: (str) -> bool
    try:
        file = open("./chrmod/config/" + fileName + ".json", "r")
        data = json.load(file)
        file.close()
        Client.instance.mPrefix = data["prefix"]
        print(data)
        Platform.SetPlatform(data["platform"])
        InputMode.SetInputMode(data["inputMode"])
        for key, value in data["modules"].items():
            for module in ModuleManager.modules:
                if module.name == key:
                    module.key = value.get("key", module.key)
                    if module.open:
                        ModuleManager.ChangeModuleState(module, True, value["args"], False)
    except:
        return False
    return True

def SaveConfig(fileName, reload=False): #type: (str, bool) -> None
    filePath = "./chrmod/config/"
    if not os.path.exists(filePath):
        os.makedirs(os.path.dirname(filePath))
    file = open(filePath + fileName + ".json", "w")
    data = {"prefix": Client.instance.mPrefix, "platform": 1, "inputMode": 3, "modules": { }}
    for module in ModuleManager.modules:
        data["modules"][module.name] = {
            "key": module.key,
            "open": module.open,
            "args": module.args
        }
    json.dump(data, file)
    file.close()
    if reload:
        LoadConfig(fileName)