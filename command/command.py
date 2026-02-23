# -*- coding: utf-8 -*-
# author Eison 
# 2024/04/21

from abc import abstractmethod

class Command:
    def __init__(self, name, description, usage, aliases):
        self.name = name
        self.description = description
        self.usage = usage
        self.aliases = aliases

    @abstractmethod
    def execute(self, args):
        # type: (list[str]) -> bool
        pass

    def __str__(self):
        return "Command(name=%s, description=%s, usage=%s, aliases=%s)" % (self.name, self.description, self.usage, self.aliases)