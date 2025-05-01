# -*- coding: utf-8 -*-

from ..command import Command
import _utility # type: ignore
import fop # type: ignore
import os

class ScriptsCommand(Command):
    def __init__(self):
        super(ScriptsCommand, self).__init__("scripts", "Run python script in minecraft game.", [ ])
        self.path = os.path.abspath(os.getcwd())

        _utility.switchAnimation(0)

    def execute(self, args):
        if len(args) < 1: 
            return False
        
        with open(args[0], "r") as f:
            code = compile("__args__ = %r\n" % (args[1:],) +f.read(), "<mc script>", "exec")

        fop.new_module("", code, [self.path])

        return True