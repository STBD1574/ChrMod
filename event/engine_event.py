# -*- coding: utf-8 -*-

import mod.common.system.eventConf as eventConf
import notify

class EngineEvent(object):
    def __init__(self, event_id, event_data):
        self._event_id = event_id
        self._event_data = event_data

    @property
    def event_data(self):
        return self._event_data

    @staticmethod
    def get_engine_event_id(python_event_id):
        # type: (str) -> int | None
        """
        Get the C++ engine event ID from the event ID string.
        :param python_event_id: The Python event ID string, just like "Minecraft:Engine:ActorAcquiredItemClientEvent"
        :return: The C++ engine event ID.
        """
        return eventConf.GetEngineClientEventID(python_event_id)

    def set_cancelled(self, cancelled):
        # type: (bool) -> None
        """
        Set the event as cancelled or not.
        """
        cpp_id = self.get_engine_event_id(self._event_id)

        if not cpp_id:
            return False
        
        return notify.set_event_canceled(self._bus_id, cpp_id, cancelled)