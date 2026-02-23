# -*- coding: utf-8 -*-
import random
import string
import mod.client.extraClientApi as clientApi
import Client

if not Client.instance:
    clientApi.RegisterSystem("Minecraft", ''.join(random.sample(string.ascii_letters + string.digits, random.randint(8, 16))), "ChrMod.Client.Main")
    print(" ====== ChrMod Init <author Eison> ======")