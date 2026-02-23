# -*- coding: utf-8 -*-
# author Eison
# 2025/02/08

from . import listener
from . import client_events

class ClientChatHandler:
    def __init__(self):
        listener.listen_for_event(self)

    @listener.engine(client_events.ClickChatSendClientEvent, 10)
    def on_client_chat(self, args):
        message = args["message"] # type: str
