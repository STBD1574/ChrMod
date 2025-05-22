# -*- coding: utf-8 -*-

from collections import defaultdict
import mod.common.system.eventConf as eventConf
import notify

class EventRegistry(object):
    def __init__(self, bus_id):
        self._bus_id = bus_id # 1 for client
        self._registered_event_ids = set() # type: set[str] # use set to remove duplicate
        self._event_handlers = defaultdict(list) # type: dict[str, list[EngineEventHandler]]

    @staticmethod
    def get_engine_event_id(event_id):
        # type: (str) -> int | None
        """
        Get the C++ engine event ID from the event ID string.
        :param event_id: The Python event ID string, just like "Minecraft:Engine:ActorAcquiredItemClientEvent"
        :return: The C++ engine event ID.
        """
        return eventConf.GetEngineClientEventID(event_id)

    def register_handler(self, event_id, event_handler):
        # type: (str, EngineEventHandler) -> bool
        cpp_id = self.get_engine_event_id(event_id)

        # if register an undefined event
        if not cpp_id:
            return False
        
        # register event id so that it can be listened to by the C++ engine
        if event_id not in self._registered_event_ids:
            self._registered_event_ids.append(event_id)
            notify.register_event_id(self._bus_id, cpp_id)

        if event_handler in self._event_handlers[event_id]:
            return False
        
        self._event_handlers[event_id].append(event_handler)

        return True