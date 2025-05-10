# -*- coding: utf-8 -*-

import mod.common.eventUtil as eventUtil # type: ignore    

def listen_for_event(name_space, system_name, event_name, instance, func, priority=0):
    # type: (str, str, str, object, callable, int) -> None
    eventUtil.instance.ListenForEventClient(name_space, system_name, event_name, instance, func, priority, True)

def un_listen_for_event(name_space, system_name, event_name, instance, func, priority=0):
    # type: (str, str, str, object, callable, int) -> None
    eventUtil.instance.UnListenForEventClient(name_space, system_name, event_name, instance, func, priority, True)

def listen_for_engine_event(eventName, instance, func, priority=0):
    # type: (str, object, callable, int) -> None
    eventUtil.instance.ListenForEngineClient(eventName, instance, func, priority, False)

def un_listen_for_engine_event(eventName, instance, func, priority=0):
    # type: (str, object, callable, int) -> None
    eventUtil.instance.UnListenForEngineClient(eventName, instance, func, priority, False)