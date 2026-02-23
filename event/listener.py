# -*- coding: utf-8 -*-
# author Eison
# 2025/02/08

from .. import pyimport

eventUtil = pyimport.import_module("mod.common.eventUtil") # import mod.common.eventUtil as eventUtil

ENGINE_NAME_SPACE = "Minecraft"
ENGINE_SYSTEM_NAME = "Engine"

class Event:
    def __init__(self, name_space, system_name, event_name, priority=0):
        self.name_space = name_space
        self.system_name = system_name
        self.event_name = event_name
        self.priority = priority


def engine(event_name, priority=0):
    def binding(func):
        func.binding_event = Event(ENGINE_NAME_SPACE, ENGINE_SYSTEM_NAME, event_name, priority)
        return func
    
    return binding

def custom(event_name, system_name, name_space, priority=0):
    def binding(func):
        func.binding_event = Event(name_space, system_name, event_name, priority)
        return func
    
    return binding

def listen_for_event(instance):
    for key in dir(instance):
        func = getattr(instance, key)
        if hasattr(func, "binding_event") and isinstance(func.binding_event, Event):
            binding = func.binding_event # type: Event
            eventUtil.instance.ListenForEventClient(
                binding.name_space,
                binding.system_name,
                binding.event_name,
                instance,
                func, 
                binding.priority
            )
        
def UnListenForEvent(instance):
    for key in dir(instance):
        func = getattr(instance, key)
        if hasattr(func, "binding_event") and isinstance(func.binding_event, Event):
            binding = func.binding_event # type: Event
            eventUtil.instance.UnListenForEventClient(
                binding.name_space,
                binding.system_name,
                binding.event_name,
                instance,
                func,
                binding.priority
            )