# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import mod.common.eventUtil as eventUtil # type: ignore

class EventListener(object):
    """
    Advanced event listener encapsulation.
    """
    __metaclass__ = ABCMeta

    ENGINE_NAME_SPACE = "Minecraft"
    ENGINE_SYSTEM_NAME = "Engine"

    def __init__(self):
        self._listen_for_event_list = [] # type: list[tuple[str, str, str, int]]

    def listen_for_event(self, name_space, system_name, event_name, priority=0):
        # type: (str, str, str, int) -> None
        """
        Listen for a custom game event.
        """
        eventUtil.instance.ListenForEventClient(name_space, system_name, event_name, self, self.on_event, priority, True)
        self._listen_for_event_list.append((name_space, system_name, event_name, priority))

    def un_listen_for_event(self, name_space, system_name, event_name, priority=0):
        # type: (str, str, str, int) -> None
        """
        Stop listening for a custom game event.
        """
        eventUtil.instance.UnListenForEventClient(name_space, system_name, event_name, self, self.on_event, priority, True)
        self._listen_for_event_list.remove((name_space, system_name, event_name, priority))

    def listen_for_engine_event(self, eventName, priority=0):
        # type: (str, int) -> None
        """
        Listen for a engine game event.
        """
        self.listen_for_event(self.ENGINE_NAME_SPACE, self.ENGINE_SYSTEM_NAME, eventName, priority)

    def un_listen_for_engine_event(self, eventName, priority=0):
        # type: (str, int) -> None
        """
        Stop listening for a engine game event.
        """
        self.un_listen_for_event(self.ENGINE_NAME_SPACE, self.ENGINE_SYSTEM_NAME, eventName, priority)

    def create(self):
        # type: () -> None
        """
        This method is called when the listener is created.
        """

    def destroy(self):
        # type: () -> None
        """
        This method is called when the listener is destroyed.
        """
        for event in self._listen_for_event_list:
            self.un_listen_for_event(*event)

        del self._listen_for_event_list[:]

    @abstractmethod
    def on_event(self, args=None):
        # type: (dict) -> None
        """
        This method is called when an event is triggered.
        """
        pass

def init():
    from .handlers.on_client_chat import OnClientChat

    listeners = [
        OnClientChat()
    ]