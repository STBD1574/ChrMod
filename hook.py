# -*- coding: utf-8 -*-
# author Eison
# 2025/02/08

import functools
from . import pyimport

inspect = pyimport.import_module('inspect') # import inspect

class Hook:
    def __init__(self):
        self.function_hooks = { }

    def function_hook(self, original, hook):
        # type: (callable, callable) -> callable
        '''
        Add a hook to a function.
        :param original: The original function to be hooked.
        :param hook: The hook function to be called instead of the original.
        :return: The original function.
        '''

        if original in self.function_hooks:
            raise ValueError('Function already has a hook.')
        
        func_name = original.__name__
        module = inspect.getmodule(original) or __builtins__

        original_func = getattr(module, func_name, original)
        self.function_hooks[original] = original_func

        @functools.wraps(original_func)
        def wrapper(*args, **kwargs):
            return hook(original_func, *args, **kwargs)

        try:
            setattr(module, func_name, wrapper)
        except AttributeError:
            raise AttributeError('Cannot hook function: %s' % func_name)

        return original
    
    def function_unhook(self, original):
        # type: (callable) -> None
        '''
        Remove a hook from a function.
        :param original: The original function to be unhooked.
        :return: None.
        '''

        if original not in self.function_hooks:
            raise ValueError('Function does not have a hook.')

        original_func = self.function_hooks[original]
        func_name = original_func.__name__
        module = inspect.getmodule(original_func) or __builtins__

        try:
            setattr(module, func_name, original_func)
        except AttributeError:
            raise AttributeError('Cannot unhook function: %s' % func_name)

        del self.function_hooks[original]

instance = Hook()

def function_hook(original, hook):
    # type: (callable, callable) -> callable
    global instance
    return instance.function_hook(original, hook)

def function_unhook(original):
    # type: (callable) -> None
    global instance
    instance.function_unhook(original)